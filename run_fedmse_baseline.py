#!/usr/bin/env python
"""
FedHome_Spark - Run FedMSE Full-Scale Baseline
This script runs the FedMSE baseline experiment directly without Jupyter
"""

import sys
import os
import json
import numpy as np
import torch
import copy
from datetime import datetime
import random
import logging

# Change to baseline/src directory
os.chdir('baseline/src')
sys.path.insert(0, '.')

from Model import Shrink_Autoencoder
from DataLoader import load_data, IoTDataset, IoTDataProccessor
from Trainer import ClientTrainer, GlobalAggregator
from Evaluator import Evaluator
from torch.utils.data import DataLoader, ConcatDataset

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuration
NUM_PARTICIPANTS = 0.5      # 50% clients per round
EPOCH = 100                  # Local epochs per round
NUM_ROUNDS = 20              # Global communication rounds
LR_RATE = 1e-5               # Learning rate
SHRINK_LAMBDA = 10           # SAE regularization
NETWORK_SIZE = 50            # Number of clients (full-scale)
BATCH_SIZE = 12
DIM_FEATURES = 115           # N-BaIoT feature dimension

print("="*60)
print("FEDMSE FULL-SCALE BASELINE EXPERIMENT")
print("="*60)
print(f"Clients: {NETWORK_SIZE}")
print(f"Rounds: {NUM_ROUNDS}")
print(f"Local Epochs: {EPOCH}")
print(f"Participant Ratio: {NUM_PARTICIPANTS*100}%")
print("="*60)

# Load configuration
print("\nLoading configuration...")
config_file = "Configuration/scen2-nba-iot-50clients.json"
with open(config_file, "r") as f:
    config = json.load(f)
print(f"Loaded: {config_file}")
print(f"Data path: {config['data_path']}")

# Prepare client data
print("\nPreparing client data...")
random.seed(42)
devices_list = random.sample(config['devices_list'], NETWORK_SIZE)
client_info = []

for i, device in enumerate(devices_list):
    normal_data_path = os.path.join(config['data_path'], device["normal_data_path"])
    abnormal_data_path = os.path.join(config['data_path'], device["abnormal_data_path"])
    test_normal_data_path = os.path.join(config['data_path'], device["test_normal_data_path"])
    
    # Load data
    normal_data = load_data(normal_data_path)
    normal_data = normal_data.sample(frac=1).reset_index(drop=True)
    abnormal_data = load_data(abnormal_data_path)
    abnormal_data = abnormal_data.sample(frac=1).reset_index(drop=True)
    new_normal_data = load_data(test_normal_data_path)
    
    # Split data
    train_normal_size = int(0.4 * len(normal_data))
    valid_normal_size = int(0.1 * len(normal_data))
    dev_normal_size = int(0.4 * len(normal_data))
    
    train_normal_data = normal_data[:train_normal_size]
    valid_normal_data = normal_data[train_normal_size:train_normal_size+valid_normal_size]
    dev_normal_data = normal_data[train_normal_size+valid_normal_size:train_normal_size+valid_normal_size+dev_normal_size]
    test_normal_data = normal_data[train_normal_size+valid_normal_size+dev_normal_size:]
    
    # Preprocess
    data_processor = IoTDataProccessor(scaler="standard")
    processed_train_data, train_label = data_processor.fit_transform(train_normal_data)
    processed_valid_data, valid_label = data_processor.transform(valid_normal_data)
    processed_test_data, test_label = data_processor.transform(test_normal_data)
    processed_abnormal_data, abnormal_label = data_processor.transform(abnormal_data, type="abnormal")
    processed_new_normal_data, new_normal_label = data_processor.transform(new_normal_data)
    
    processed_test_data = np.concatenate([processed_test_data, processed_new_normal_data], axis=0)
    test_dataset = IoTDataset(processed_test_data, np.concatenate([test_label, new_normal_label], axis=0))
    
    train_dataset = IoTDataset(processed_train_data, train_label)
    valid_dataset = IoTDataset(processed_valid_data, valid_label)
    abnormal_dataset = IoTDataset(processed_abnormal_data, abnormal_label)
    test_dataset = ConcatDataset([test_dataset, abnormal_dataset])
    
    client_info.append({
        "device": device['name'],
        "train_loader": DataLoader(dataset=train_dataset, batch_size=BATCH_SIZE, pin_memory=True),
        "valid_loader": DataLoader(dataset=valid_dataset, batch_size=BATCH_SIZE, pin_memory=True),
        "test_loader": DataLoader(dataset=test_dataset, batch_size=BATCH_SIZE, pin_memory=True),
        "dev_normal_dataset": dev_normal_data
    })
    
    if (i + 1) % 10 == 0:
        print(f"  Prepared {i+1}/{NETWORK_SIZE} clients...")

print(f"Prepared data for {len(client_info)} clients")

# Initialize global model
print("\nInitializing global model (SAE-CEN + MSEAvg)...")
global_model = Shrink_Autoencoder(
    input_dim=DIM_FEATURES,
    output_dim=DIM_FEATURES,
    shrink_lambda=SHRINK_LAMBDA,
    latent_dim=11,
    hidden_neus=50
)

global_aggregator = GlobalAggregator(global_model, update_type="mse_avg")

# Create development dataset
min_len = min([len(client['dev_normal_dataset']) for client in client_info])
dev_dataset = []
for client in client_info:
    sample_data = client['dev_normal_dataset'].sample(n=min_len)
    dev_dataset.append(sample_data)
dev_dataset = np.concatenate(dev_dataset, axis=0)
global_aggregator.create_dev_dataset({"dataset": dev_dataset})
print(f"Development dataset: {len(dev_dataset)} samples")

# Training loop
print("\n" + "="*60)
print("STARTING FEDMSE TRAINING")
print("="*60)

all_results = []
min_val_loss = float("inf")
global_worse = 0
global_patience = 3

for round_num in range(NUM_ROUNDS):
    round_start = datetime.now()
    
    # Select clients for this round
    selected_idx = random.sample(
        [i for i in range(len(client_info))], 
        int(NUM_PARTICIPANTS * len(client_info))
    )
    selected_clients = [client_info[i] for i in selected_idx]
    
    total_training_samples = sum([len(client['train_loader'].dataset) for client in selected_clients])
    
    # Train selected clients
    client_weights = []
    for i, client in enumerate(selected_clients):
        device_trainer = ClientTrainer(
            model=global_aggregator.model,
            save_dir=f"../Checkpoint/Spark/FullScale/Client_{i}",
            epoch=EPOCH,
            lr_rate=LR_RATE,
            update_type="mse_avg"
        )
        device_trainer.run(client["train_loader"], client["valid_loader"])
        client_weights.append((
            copy.deepcopy(device_trainer.model.state_dict()),
            total_training_samples,
            len(client["train_loader"].dataset)
        ))
    
    # Aggregate global model
    global_aggregator.update(local_models=client_weights)
    
    # Evaluate
    evaluator = Evaluator(global_aggregator.model, metric="AUC", model_type="hybrid")
    round_results = {
        'round': round_num + 1,
        'global_loss': global_aggregator.val_loss,
        'selected_clients': selected_idx,
        'training_time': (datetime.now() - round_start).total_seconds()
    }
    
    for i, client in enumerate(client_info):
        auc_score, _, _ = evaluator.evaluate(client["test_loader"], client["train_loader"])
        round_results[f"client_{i}_auc"] = auc_score
    
    round_results['avg_auc'] = np.mean([
        round_results[f"client_{i}_auc"] for i in range(len(client_info))
    ])
    
    all_results.append(round_results)
    
    # Print progress
    print(f"Round {round_num+1}/{NUM_ROUNDS} | Loss: {global_aggregator.val_loss:.4f} | Avg AUC: {round_results['avg_auc']:.4f} | Time: {round_results['training_time']:.1f}s")
    
    # Early stopping check
    if global_aggregator.val_loss < min_val_loss:
        min_val_loss = global_aggregator.val_loss
        global_worse = 0
    else:
        global_worse += 1
        if global_worse > global_patience:
            print("Early stopping triggered!")
            break

print("\n" + "="*60)
print("TRAINING COMPLETED")
print("="*60)

# Save results
os.makedirs('../outputs/results', exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
results_path = f'../outputs/results/fedmse_fullscale_{timestamp}.json'
with open(results_path, 'w') as f:
    json.dump(all_results, f, indent=2)
print(f"Results saved to: {results_path}")

# Print summary
final_round = all_results[-1]
final_aucs = [final_round[f'client_{i}_auc'] for i in range(len(client_info))]
losses = [r['global_loss'] for r in all_results]

print("\n" + "="*60)
print("EXPERIMENT SUMMARY")
print("="*60)
print(f"Completed Rounds: {len(all_results)}")
print(f"Final Average AUC: {final_round['avg_auc']:.6f}")
print(f"Final Min AUC: {min(final_aucs):.6f}")
print(f"Final Max AUC: {max(final_aucs):.6f}")
print(f"Initial Loss: {losses[0]:.4f}")
print(f"Final Loss: {losses[-1]:.4f}")
print(f"Loss Reduction: {(1 - losses[-1]/losses[0])*100:.1f}%")
print(f"Total Training Time: {sum([r['training_time'] for r in all_results])/60:.1f} minutes")
print("="*60)
print("\n✅ FedMSE Full-Scale Baseline Complete!")
