# FedHome Project Context

**Student:** Md. Raihan Sobhan  
**Course:** Big Data Analytics  
**Project:** FedHome - Spark-Enhanced Federated Learning for IoT Botnet Detection

---

## 📌 Problem Statement

IoT botnet attacks (Mirai, Gafgyt) pose significant security threats. Traditional centralized ML approaches require collecting all data at a central server, which raises privacy concerns and is impractical for distributed IoT environments.

### Challenges

1. **Data Privacy:** IoT devices generate sensitive data that cannot be shared centrally
2. **Non-IID Data:** Different IoT gateways have heterogeneous device mixes and traffic patterns
3. **Scalability:** Large-scale IoT deployments require distributed computing
4. **Model Performance:** Standard federated learning struggles with Non-IID data distributions

---

## 🎯 Project Goals

### Primary Objective
Develop **FedHome**, a novel federated learning framework that:
- Uses **Apache Spark** for distributed data processing
- Implements **device-type-aware clustering** to handle Non-IID data
- Achieves better anomaly detection than baseline FedMSE

### Technical Objectives
1. Reproduce FedMSE baseline results
2. Implement Spark-based distributed preprocessing
3. Add Spark MLlib clustering layer
4. Run cluster-aware federated training
5. Evaluate on N-BaIoT dataset (50 gateways, Non-IID)

---

## 📚 Background

### FedMSE Baseline

FedMSE (Nguyen & Beuran, 2025) is a federated learning approach for IoT botnet detection using:
- **Shrink Autoencoder (SAE-CEN):** Compressed latent representation
- **MSEAvg Aggregation:** Mean squared error-based model averaging
- **Development Dataset:** Shared validation set for consistent evaluation

**Reported Results:**
- IID scenario: ~97% AUC
- Non-IID scenario: ~95% AUC (with high variance)

### FedHome Innovation

FedHome extends FedMSE with:

| Aspect | FedMSE | FedHome (Proposed) |
|--------|--------|-------------------|
| Data Processing | Pandas (single-node) | Apache Spark (distributed) |
| Gateway Selection | Random | Cluster-aware |
| Model Specialization | Single global model | Per-cluster specialized models |
| Device-Type Signal | Ignored | Used for clustering |
| Non-IID Robustness | Moderate | High |

---

## 🏗️ FedHome Architecture

### 4-Phase Pipeline

```
Phase 1: Spark Data Processing
├── Load N-BaIoT data into Spark DataFrames
├── Parallel feature scaling
└── Distributed statistics aggregation

Phase 2: Spark MLlib Clustering
├── Device-type profiling (per gateway)
├── JS-Divergence distance computation
└── Bisecting K-Means clustering

Phase 3: Cluster-Aware Federated Training
├── Assign clients to clusters
├── Run FedMSE per cluster (parallel)
└── Track per-cluster metrics

Phase 4: Ensemble Merge
├── Weighted model aggregation
├── Final evaluation
└── Result generation
```

---

## 📊 Dataset

### N-BaIoT Dataset

| Attribute | Value |
|-----------|-------|
| Devices | 9 IoT devices |
| Device Types | Cameras, Doorbells, Thermostats, Baby Monitors |
| Attacks | Mirai + Gafgyt botnet variants |
| Features | 115 network traffic features |
| Scenarios | IID and Non-IID distributions |

### Non-IID Scenario (50 Clients)

- **Distribution:** Dirichlet-based allocation
- **Heterogeneity:** JS divergence ≈ 0.83 (high)
- **Challenge:** Each gateway has different device-type mix

---

## 🔧 Technology Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| Distributed Computing | Apache Spark 3.5+ | Industry-standard big data framework |
| ML Library | Spark MLlib | Scalable clustering algorithms |
| Deep Learning | PyTorch 2.0+ | Flexible neural network framework |
| Data Processing | Spark DataFrames | Distributed data manipulation |
| Clustering | Bisecting K-Means | Scalable hierarchical clustering |
| Visualization | Matplotlib, Seaborn | Publication-quality figures |

---

## 📈 Evaluation Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| AUC-ROC | Area under ROC curve | ≥0.98 |
| Loss Convergence | Global reconstruction loss | Decreasing trend |
| Clustering Quality | Silhouette score | >0.5 |
| Speedup | Spark vs. pandas | ≥2x |
| Scalability | 50+ clients | Full completion |

---

## 📝 Presentation Notes

### Key Points to Emphasize

1. **Apache Spark Integration:** "We used Apache Spark for distributed data processing and clustering"
2. **Big Data Focus:** "Spark enables scaling to hundreds of clients"
3. **Novel Clustering:** "Device-type-aware clustering addresses Non-IID challenge"
4. **Privacy-Preserving:** "No raw data sharing - only model weights"

### Architecture Diagram

Include the 4-phase pipeline diagram showing:
- Spark DataFrames for distributed processing
- Spark MLlib for clustering
- Parallel cluster-aware training
- Ensemble merge

---

## 📁 Repository Structure

```
FedHome_Spark/
├── README.md              # Project overview
├── PLAN.md                # Implementation plan
├── baseline/              # FedMSE baseline
├── notebooks/             # Jupyter notebooks
├── outputs/               # Results and figures
├── spark_env/             # Spark configuration
└── Knowledge_Base/        # This folder
```

---

## 🔗 References

1. Nguyen, T. T., & Beuran, R. (2025). FedMSE: Federated Learning with Mean Squared Error Averaging for IoT Botnet Detection.
2. N-BaIoT Dataset: https://archive.ics.uci.edu/ml/datasets/N_BaIoT
3. Apache Spark: https://spark.apache.org/
4. Spark MLlib: https://spark.apache.org/mllib/

---

**Last Updated:** 2026-10-07  
**Status:** Active Development
