# FedHome: Apache Spark-Based Federated Learning for IoT Botnet Detection

**Student:** Md. Raihan Sobhan  
**Course:** Big Data Analytics  
**Project:** FedHome - Spark-Enhanced Federated Learning System

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
├── PLAN.md                   # Implementation plan
├── baseline/                 # FedMSE baseline repository
│   ├── src/
│   ├── Data/
│   └── ...
├── notebooks/
│   ├── 01_spark_setup.ipynb           # Spark installation & testing
│   ├── 02_fedmse_spark_fullscale.ipynb # FedMSE with Spark
│   └── 03_fedhome_spark_clustering.ipynb # FedHome clustering
├── outputs/
│   ├── figures/              # Generated figures
│   ├── results/              # JSON results
│   └── logs/                 # Training logs
├── spark_env/                # Spark configuration
└── Knowledge_Base/
    ├── Context.md            # Project requirements
    └── Initial_Plan.md       # Initial implementation plan
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

### Running the Project

1. **Spark Setup Test:**
   ```bash
   jupyter notebook notebooks/01_spark_setup.ipynb
   ```

2. **FedMSE Full-Scale with Spark:**
   ```bash
   jupyter notebook notebooks/02_fedmse_spark_fullscale.ipynb
   ```

3. **FedHome Clustering:**
   ```bash
   jupyter notebook notebooks/03_fedhome_spark_clustering.ipynb
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

## 📈 Expected Results

| Metric | FedMSE Baseline | FedHome (Expected) |
|--------|-----------------|-------------------|
| Average AUC | ~0.97 | ~0.98+ |
| Non-IID Robustness | Moderate | High |
| Scalability | Limited | Spark-enhanced |
| Device-Type Awareness | No | Yes |

---

## 📝 License

This project is for academic purposes (Big Data Analytics course).

---

## 📧 Contact

**Md. Raihan Sobhan**  
Big Data Analytics Course  
Project: FedHome - Spark-Enhanced Federated Learning
