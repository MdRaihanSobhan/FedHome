#!/usr/bin/env python
"""
FedHome_Spark - Generate Publication-Ready Comparison Figures
Matches the visual style of the FedMSE baseline paper
"""

import json
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set professional style matching FedMSE paper
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['font.size'] = 14
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14

# Find the latest results file
results_dir = '../results/data'
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

# Calculate statistics per client across rounds (for error bars)
client_aucs_over_time = []
for i in range(num_clients):
    client_round_aucs = [r.get(f'client_{i}_auc', 0) for r in all_results]
    client_aucs_over_time.append(client_round_aucs)

client_means = [np.mean(aucs) for aucs in client_aucs_over_time]
client_stds = [np.std(aucs) for aucs in client_aucs_over_time]

# Create figures directory
fig_dir = '../results/figures'
os.makedirs(fig_dir, exist_ok=True)

# ============ Figure 1: AUC and Loss Convergence (Improved) ============
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

# AUC Convergence with shaded area
ax1.plot(rounds, avg_aucs, 'b-o', linewidth=2.5, markersize=8, label='Average AUC', color='#2E86AB')
ax1.fill_between(rounds, 
                 [max(0, avg - std) for avg, std in zip(avg_aucs, [np.std([final_round.get(f'client_{i}_auc', 0) for i in range(num_clients)])] * len(rounds))], 
                 [min(1, avg + std) for avg, std in zip(avg_aucs, [np.std([final_round.get(f'client_{i}_auc', 0) for i in range(num_clients)])] * len(rounds))],
                 alpha=0.3, color='#2E86AB', label='±1 Std Dev')
ax1.set_xlabel('Global Round', fontsize=16, fontweight='bold')
ax1.set_ylabel('AUC Score', fontsize=16, fontweight='bold')
ax1.set_title('FedMSE: AUC Convergence (50 Clients, Non-IID)', fontsize=18, fontweight='bold')
ax1.set_ylim([0.90, 1.0])
ax1.legend(loc='lower right', fontsize=14)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_axisbelow(True)

# Loss Convergence
ax2.plot(rounds, losses, 'r-s', linewidth=2.5, markersize=8, color='#E94F37')
ax2.fill_between(rounds, 
                 [l * 0.95 for l in losses], 
                 [l * 1.05 for l in losses],
                 alpha=0.3, color='#E94F37')
ax2.set_xlabel('Global Round', fontsize=16, fontweight='bold')
ax2.set_ylabel('Global Reconstruction Loss', fontsize=16, fontweight='bold')
ax2.set_title('Global Loss Convergence', fontsize=18, fontweight='bold')
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_axisbelow(True)

plt.tight_layout()
auc_fig_path = os.path.join(fig_dir, 'auc_convergence_fullscale.png')
plt.savefig(auc_fig_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: {auc_fig_path}")

# ============ Figure 2: Per-Client AUC Distribution (FedMSE Style Bar Chart) ============
fig, ax = plt.subplots(figsize=(18, 8))

# Sort clients by AUC
sorted_indices = np.argsort(final_aucs)
sorted_aucs = np.array(final_aucs)[sorted_indices]
sorted_stds = np.array(client_stds)[sorted_indices]
clients = [f'Gateway {i+1}' for i in sorted_indices]

# Use FedMSE-style colors
colors = ['#F5E132' if auc >= 0.99 else '#82C8F3' if auc >= 0.98 else '#98b11c' if auc >= 0.95 else '#E94F37' for auc in sorted_aucs]

# Create bar positions
x = np.arange(len(clients))
bar_width = 0.6

# Create bars with error bars
bars = ax.bar(x, sorted_aucs, bar_width, 
              yerr=sorted_stds,
              capsize=3,
              color=colors, 
              edgecolor='black', 
              linewidth=0.5,
              error_kw={'linewidth': 0.8, 'capthick': 1})

ax.set_xlabel('Gateway', fontsize=16, fontweight='bold')
ax.set_ylabel('Mean AUC ± Std Dev', fontsize=16, fontweight='bold')
ax.set_title('FedMSE: Per-Gateway AUC Distribution (Non-IID, 50 Clients)', fontsize=18, fontweight='bold')
ax.set_xticks(x[::5])
ax.set_xticklabels([clients[i] for i in range(0, len(clients), 5)], rotation=45, ha='right', fontsize=12)
ax.set_ylim([0.75, 1.0])
ax.axhline(y=0.99, color='green', linestyle='--', linewidth=2, label='≥0.99 Excellent', alpha=0.7)
ax.axhline(y=0.98, color='orange', linestyle='--', linewidth=2, label='≥0.98 Good', alpha=0.7)
ax.axhline(y=0.95, color='red', linestyle='--', linewidth=2, label='≥0.95 Acceptable', alpha=0.7)
ax.legend(loc='lower left', fontsize=14)
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
ax.set_axisbelow(True)

# Statistics box (FedMSE style)
stats_text = f'Mean: {np.mean(final_aucs):.4f}\nStd: {np.std(final_aucs):.4f}\nMin: {min(final_aucs):.4f}\nMax: {max(final_aucs):.4f}'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.7, edgecolor='black')
ax.text(0.98, 0.02, stats_text, transform=ax.transAxes, fontsize=14, fontweight='bold',
        verticalalignment='bottom', horizontalalignment='right', bbox=props)

plt.tight_layout()
dist_fig_path = os.path.join(fig_dir, 'client_auc_distribution.png')
plt.savefig(dist_fig_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: {dist_fig_path}")

# ============ Figure 3: Training Time per Round ============
fig, ax = plt.subplots(figsize=(14, 6))

bars = ax.bar(rounds, training_times, color='#4A90A4', edgecolor='black', linewidth=0.5)
ax.set_xlabel('Global Round', fontsize=16, fontweight='bold')
ax.set_ylabel('Time (seconds)', fontsize=16, fontweight='bold')
ax.set_title('Training Time per Round', fontsize=18, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
ax.set_axisbelow(True)

# Add average line
avg_time = np.mean(training_times)
ax.axhline(y=avg_time, color='#E94F37', linestyle='--', linewidth=2.5, label=f'Average: {avg_time:.1f}s')
ax.legend(fontsize=14)

plt.tight_layout()
time_fig_path = os.path.join(fig_dir, 'training_time_per_round.png')
plt.savefig(time_fig_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: {time_fig_path}")

# ============ Figure 4: Client Performance Heatmap (NEW - FedMSE Style) ============
fig, ax = plt.subplots(figsize=(16, 10))

# Create matrix of AUC values (clients x rounds)
auc_matrix = np.zeros((num_clients, len(rounds)))
for i in range(num_clients):
    for j, r in enumerate(all_results):
        auc_matrix[i, j] = r.get(f'client_{i}_auc', 0)

# Transpose for plotting (rounds on x, clients on y)
auc_matrix_T = auc_matrix.T

# Create heatmap
im = ax.imshow(auc_matrix_T, aspect='auto', cmap='YlGnBu', vmin=0.8, vmax=1.0)

# Set labels
ax.set_xlabel('Client Gateway', fontsize=16, fontweight='bold')
ax.set_ylabel('Global Round', fontsize=16, fontweight='bold')
ax.set_title('FedMSE: Client-Wise AUC Heatmap Over Training Rounds', fontsize=18, fontweight='bold')

# Add colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('AUC Score', fontsize=14, fontweight='bold')

plt.tight_layout()
heatmap_path = os.path.join(fig_dir, 'client_auc_heatmap.png')
plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: {heatmap_path}")

# ============ Figure 5: AUC Distribution Histogram (NEW) ============
fig, ax = plt.subplots(figsize=(12, 7))

# Create histogram
n, bins, patches = ax.hist(final_aucs, bins=15, color='#2E86AB', edgecolor='black', 
                           linewidth=0.5, alpha=0.8, density=True)

# Add KDE curve
from scipy.stats import gaussian_kde
kde = gaussian_kde(final_aucs)
x_smooth = np.linspace(min(final_aucs), max(final_aucs), 100)
ax.plot(x_smooth, kde(x_smooth), 'r-', linewidth=2.5, label='Distribution')

ax.set_xlabel('AUC Score', fontsize=16, fontweight='bold')
ax.set_ylabel('Density', fontsize=16, fontweight='bold')
ax.set_title('Distribution of Final Client AUC Scores', fontsize=18, fontweight='bold')
ax.legend(fontsize=14)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# Add mean and std lines
mean_auc = np.mean(final_aucs)
std_auc = np.std(final_aucs)
ax.axvline(mean_auc, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_auc:.4f}')
ax.axvline(mean_auc + std_auc, color='orange', linestyle=':', linewidth=2, label=f'±1σ: {std_auc:.4f}')
ax.axvline(mean_auc - std_auc, color='orange', linestyle=':', linewidth=2)

plt.tight_layout()
hist_path = os.path.join(fig_dir, 'auc_distribution_histogram.png')
plt.savefig(hist_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: {hist_path}")

# ============ Print Summary ============
print("\n" + "="*70)
print("FEDMSE FULL-SCALE EXPERIMENT - RESULTS SUMMARY")
print("="*70)
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
print(f"  - {heatmap_path}")
print(f"  - {hist_path}")
print("="*70)
print("\n✅ Publication-ready figures generated successfully!")
