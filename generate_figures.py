#!/usr/bin/env python
"""
FedHome_Spark - Generate Result Figures from FedMSE Experiment
"""

import json
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Find the latest results file
results_dir = 'baseline/outputs/results'
results_files = [f for f in os.listdir(results_dir) if f.startswith('fedmse_fullscale_') and f.endswith('.json')]

if not results_files:
    print("No results files found!")
    exit(1)

latest_file = sorted(results_files)[-1]
results_path = os.path.join(results_dir, latest_file)

print(f"Loading results from: {results_path}")

with open(results_path, 'r') as f:
    all_results = json.load(f)

print(f"Loaded {len(all_results)} rounds of results")

# Extract data
rounds = [r['round'] for r in all_results]
avg_aucs = [r['avg_auc'] for r in all_results]
losses = [r['global_loss'] for r in all_results]
training_times = [r['training_time'] for r in all_results]

# Get final round client AUCs
final_round = all_results[-1]
num_clients = 50
final_aucs = [final_round.get(f'client_{i}_auc', 0) for i in range(num_clients)]

# Create figures directory
fig_dir = 'outputs/figures'
os.makedirs(fig_dir, exist_ok=True)

# ============ Figure 1: AUC and Loss Convergence ============
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# AUC Convergence
ax1.plot(rounds, avg_aucs, 'b-o', linewidth=2, markersize=8, label='Average AUC')
ax1.fill_between(rounds, 
                 [min(final_aucs)] * len(rounds), 
                 [max(final_aucs)] * len(rounds),
                 alpha=0.2, color='blue', label='Min-Max Range')
ax1.set_xlabel('Global Round', fontsize=12, fontweight='bold')
ax1.set_ylabel('AUC Score', fontsize=12, fontweight='bold')
ax1.set_title('FedMSE: AUC Convergence (50 Clients, Non-IID)', fontsize=14, fontweight='bold')
ax1.set_ylim([0.90, 1.0])
ax1.legend(loc='lower right')
ax1.grid(True, alpha=0.3)

# Loss Convergence
ax2.plot(rounds, losses, 'r-s', linewidth=2, markersize=8)
ax2.set_xlabel('Global Round', fontsize=12, fontweight='bold')
ax2.set_ylabel('Global Reconstruction Loss', fontsize=12, fontweight='bold')
ax2.set_title('Global Loss Convergence', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
auc_fig_path = os.path.join(fig_dir, 'auc_convergence_fullscale.png')
plt.savefig(auc_fig_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: {auc_fig_path}")

# ============ Figure 2: Per-Client AUC Distribution ============
fig, ax = plt.subplots(figsize=(14, 6))

# Sort clients by AUC
sorted_indices = np.argsort(final_aucs)
sorted_aucs = np.array(final_aucs)[sorted_indices]
clients = [f'Client-{i+1}' for i in sorted_indices]

# Color by performance
colors = ['#2ecc71' if auc >= 0.99 else '#f39c12' if auc >= 0.98 else '#e74c3c' for auc in sorted_aucs]
bars = ax.bar(range(len(clients)), sorted_aucs, color=colors, edgecolor='black', linewidth=0.5)

ax.set_xlabel('Client ID (sorted by AUC)', fontsize=12, fontweight='bold')
ax.set_ylabel('AUC Score', fontsize=12, fontweight='bold')
ax.set_title(f'FedMSE: Per-Client AUC Distribution (Final Round {rounds[-1]})', fontsize=14, fontweight='bold')
ax.set_xticks(range(0, len(clients), 5))
ax.set_xticklabels([clients[i] for i in range(0, len(clients), 5)], rotation=45, ha='right')
ax.set_ylim([0.75, 1.0])
ax.axhline(y=0.99, color='green', linestyle='--', linewidth=1.5, label='>=0.99 Excellent')
ax.axhline(y=0.98, color='orange', linestyle='--', linewidth=1.5, label='>=0.98 Good')
ax.axhline(y=0.95, color='red', linestyle='--', linewidth=1.5, label='>=0.95 Acceptable')
ax.legend(loc='lower left')
ax.grid(True, alpha=0.3, axis='y')

# Statistics box
stats_text = f'Mean: {np.mean(final_aucs):.4f}\nStd: {np.std(final_aucs):.4f}\nMin: {min(final_aucs):.4f}\nMax: {max(final_aucs):.4f}'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.98, 0.02, stats_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom', horizontalalignment='right', bbox=props)

plt.tight_layout()
dist_fig_path = os.path.join(fig_dir, 'client_auc_distribution.png')
plt.savefig(dist_fig_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: {dist_fig_path}")

# ============ Figure 3: Training Time per Round ============
fig, ax = plt.subplots(figsize=(12, 5))

ax.bar(rounds, training_times, color='steelblue', edgecolor='black', linewidth=0.5)
ax.set_xlabel('Global Round', fontsize=12, fontweight='bold')
ax.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
ax.set_title('Training Time per Round', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

# Add average line
avg_time = np.mean(training_times)
ax.axhline(y=avg_time, color='red', linestyle='--', linewidth=2, label=f'Average: {avg_time:.1f}s')
ax.legend()

plt.tight_layout()
time_fig_path = os.path.join(fig_dir, 'training_time_per_round.png')
plt.savefig(time_fig_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: {time_fig_path}")

# ============ Print Summary ============
print("\n" + "="*60)
print("FEDMSE FULL-SCALE EXPERIMENT - RESULTS SUMMARY")
print("="*60)
print(f"Results file: {results_path}")
print(f"\nConfiguration:")
print(f"  Clients: 50 (Non-IID)")
print(f"  Global Rounds: 20")
print(f"  Local Epochs: 100")
print(f"  Participant Ratio: 50%")
print(f"\nPerformance:")
print(f"  Final Average AUC: {np.mean(final_aucs):.6f}")
print(f"  Min AUC: {min(final_aucs):.6f}")
print(f"  Max AUC: {max(final_aucs):.6f}")
print(f"  Std Dev: {np.std(final_aucs):.6f}")
print(f"\nLoss:")
print(f"  Initial: {losses[0]:.4f}")
print(f"  Final: {losses[-1]:.4f}")
print(f"  Reduction: {(1 - losses[-1]/losses[0])*100:.1f}%")
print(f"\nTraining Time:")
print(f"  Total: {sum(training_times)/60:.2f} minutes")
print(f"  Avg per round: {np.mean(training_times):.1f} seconds")
print(f"\nFigures generated:")
print(f"  - {auc_fig_path}")
print(f"  - {dist_fig_path}")
print(f"  - {time_fig_path}")
print("="*60)
print("\n✅ Result figures generated successfully!")
