# FedHome: Apache Spark-Based Federated Learning for IoT Botnet Detection

**Student:** Md. Raihan Sobhan  
**Course:** Big Data Analytics  
**Project:** FedHome - Spark-Enhanced Federated Learning System

**Last Updated:** 2026-10-07  
**Status:** ✅ Phase 1 Complete - Baseline Results Achieved

---

## 📖 Overview

FedHome is a novel federated learning framework for IoT botnet detection that extends the FedMSE (Federated Learning with Mean Squared Error averaging) baseline with **Apache Spark-based distributed computing** and **device-type-aware clustering**.

### Key Innovations

1. **Spark-Enhanced Data Processing:** Leveraging Apache Spark for large-scale distributed data preprocessing and feature engineering
2. **Device-Type Clustering:** Using Spark MLlib's Bisecting K-Means to cluster gateways by device-type distribution
3. **Cluster-Aware Federation:** Running specialized federated learning within each cluster
4. **Privacy-Preserving:** No raw data sharing - only model weights and device-type metadata

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FedHome Architecture                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1: Spark Data Processing                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Gateway 1  │  │  Gateway 2  │  │  Gateway N  │              │
│  │  (50 total) │  │             │  │             │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
│         └────────────────┴────────────────┘                      │
│                          │                                       │
│                   ┌──────▼──────┐                                │
│                   │ Spark DataFrame │                            │
│                   │ Preprocessing   │                            │
│                   └──────┬──────┘                                │
│                          │                                       │
│  Phase 2: Spark MLlib Clustering                                 │
│                   ┌──────▼──────┐                                │
│                   │ JS-Divergence │                              │
│                   │ + K-Means     │                              │
│                   └──────┬──────┘                                │
│                          │                                       │
│         ┌────────────────┼────────────────┐                     │
│         │                │                │                      │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐              │
│  │  Cluster 1  │  │  Cluster 2  │  │  Cluster K  │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
│  Phase 3: Cluster-Aware Federated Training                       │
│         │                │                │                      │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐              │
│  │ FedMSE Run  │  │ FedMSE Run  │  │ FedMSE Run  │              │
│  │ (Parallel)  │  │ (Parallel)  │  │ (Parallel)  │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
│  Phase 4: Ensemble Merge                                         │
│         └────────────────┼────────────────┘                     │
│                   ┌──────▼──────┐                                │
│                   │  Final Model │                              │
│                   └─────────────┘                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
FedHome_Spark/
├── README.md                 # This file
├── PLAN.md                   # Implementation plan (UPDATED)
├── baseline/                 # FedMSE baseline repository
│   ├── src/                 # FedMSE source code
│   └── Data/                # Dataset (50 clients, Non-IID)
├── experiments/              # Jupyter notebooks
│   ├── 01_spark_setup_simple.ipynb
│   ├── 02_fedmse_spark_fullscale.ipynb
│   └── 03_fedhome_spark_clustering.ipynb
├── scripts/                  # Python scripts
│   ├── run_fedmse_baseline.py
│   ├── generate_figures.py
│   └── test_setup.py
├── results/                  # Experiment outputs
│   ├── data/                # JSON results
│   ├── figures/             # Generated figures (300 DPI)
│   └── logs/                # Training logs
├── models/                   # Trained model checkpoints
│   └── fedmse_checkpoints/  # 20 client models
├── Knowledge_Base/           # Project documentation
│   ├── Context.md
│   └── Initial_Plan.md
└── spark_env/                # Virtual environment
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Java 8+ (for Spark)
- 10GB+ free disk space

### Installation

```bash
# Install PySpark
pip install pyspark pandas numpy torch scikit-learn matplotlib seaborn

# Verify installation
python -c "import pyspark; print(pyspark.__version__)"
```

### Running Experiments

1. **Verify Setup:**
   ```bash
   python scripts/test_setup.py
   ```

2. **Run FedMSE Baseline:**
   ```bash
   python scripts/run_fedmse_baseline.py
   ```

3. **Generate Figures:**
   ```bash
   cd scripts && python generate_figures.py
   ```

4. **Run Notebooks (Interactive):**
   ```bash
   jupyter notebook experiments/01_spark_setup_simple.ipynb
   jupyter notebook experiments/02_fedmse_spark_fullscale.ipynb
   jupyter notebook experiments/03_fedhome_spark_clustering.ipynb
   ```

---

## 📊 Dataset

- **Source:** N-BaIoT Dataset
- **Devices:** 9 IoT devices (cameras, doorbells, thermostats)
- **Attacks:** Mirai and Gafgyt botnet variants
- **Features:** 115 network traffic features
- **Clients:** 50 gateways (Non-IID distribution)

---

## 🔧 Technology Stack

| Component | Technology |
|-----------|------------|
| Distributed Computing | Apache Spark 3.5+ |
| ML Library | Spark MLlib |
| Deep Learning | PyTorch 2.0+ |
| Data Processing | Spark DataFrames, Pandas |
| Clustering | Bisecting K-Means (Spark MLlib) |
| Visualization | Matplotlib, Seaborn |

---

## 📈 Results Summary

### FedMSE Baseline (COMPLETED ✅)

| Metric | Value |
|--------|-------|
| **Clients** | 50 (Non-IID) |
| **Global Rounds** | 20 |
| **Local Epochs** | 100 |
| **Final Average AUC** | **0.9829** |
| **Min AUC** | 0.8021 |
| **Max AUC** | 1.0000 |
| **Std Dev** | 0.0325 |
| **Initial Loss** | 1.3671 |
| **Final Loss** | 0.8063 |
| **Loss Reduction** | **41.0%** |
| **Training Time** | 2.87 minutes |

### Generated Figures

- `results/figures/auc_convergence_fullscale.png` - AUC & loss convergence over 20 rounds
- `results/figures/client_auc_distribution.png` - Per-client AUC distribution with statistics
- `results/figures/training_time_per_round.png` - Training time analysis

---

## 📝 License

This project is for academic purposes (Big Data Analytics course).

---

## 📧 Contact

**Md. Raihan Sobhan**  
Big Data Analytics Course  
Project: FedHome - Spark-Enhanced Federated Learning
