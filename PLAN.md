# FedHome_Spark Implementation Plan

**Project:** FedHome - Spark-Enhanced Federated Learning for IoT Botnet Detection  
**Student:** Md. Raihan Sobhan  
**Course:** Big Data Analytics  

---

## 📋 Project Goals

1. **Reproduce FedMSE Baseline:** Validate the FedMSE paper results using the provided codebase
2. **Implement FedHome with Spark:** Extend FedMSE with Apache Spark-based distributed computing
3. **Full-Scale Evaluation:** Run experiments with 50 clients (full Non-IID scenario)
4. **Generate Publication-Ready Results:** Create figures and tables for presentation

---

## 🎯 Implementation Phases

### Phase 0: Environment Setup (Priority: HIGH)

**Tasks:**
- [ ] Install PySpark via pip
- [ ] Verify Java installation (Spark requirement)
- [ ] Create Spark session configuration
- [ ] Test Spark with simple operations

**Commands:**
```bash
# Check Java
java -version

# Install PySpark
pip install pyspark

# Test Spark
python -c "from pyspark.sql import SparkSession; print('Spark OK')"
```

**Deliverables:**
- `spark_env/spark_config.py` - Spark session configuration
- `notebooks/01_spark_setup.ipynb` - Setup verification notebook

---

### Phase 1: FedMSE Baseline Reproduction (Priority: HIGH)

**Tasks:**
- [ ] Link prepared dataset to `baseline/Data/`
- [ ] Run smoke test with 10 clients (verification)
- [ ] Run full-scale with 50 clients
- [ ] Generate baseline result figures

**Configuration:**
- Clients: 50 (Non-IID)
- Rounds: 20
- Local Epochs: 100
- Participant Ratio: 50%
- Model: SAE-CEN + MSEAvg

**Deliverables:**
- Baseline training logs
- AUC convergence figures
- Client-wise AUC comparison

---

### Phase 2: Spark-Enhanced Data Processing (Priority: MEDIUM)

**Tasks:**
- [ ] Convert data loading to Spark DataFrames
- [ ] Implement parallel feature scaling with Spark
- [ ] Use Spark for data statistics aggregation
- [ ] Benchmark vs. original pandas loading

**Code Structure:**
```python
from pyspark.sql import SparkSession
from pyspark.ml.feature import StandardScaler

# Create Spark DataFrame from N-BaIoT data
df = spark.read.csv("path/to/data/*.csv", header=True, inferSchema=True)

# Parallel preprocessing
processed_df = df.withColumn("scaled_features", StandardScaler(...))
```

**Deliverables:**
- `notebooks/02_fedmse_spark_fullscale.ipynb`
- Performance comparison (Spark vs. pandas)

---

### Phase 3: FedHome Spark Clustering (Priority: HIGH)

**Tasks:**
- [ ] Implement device-type profiling with Spark
- [ ] Compute JS-divergence using Spark UDF
- [ ] Use Spark MLlib Bisecting K-Means for clustering
- [ ] Assign clients to clusters

**Algorithm:**
```python
from pyspark.ml.clustering import BisectingKMeans

# Device-type distribution vectors
device_profiles = [...]  # Shape: (n_gateways, n_device_classes)

# Spark clustering
bm = BisectingKMeans(k=5)
model = bm.fit(device_profiles_df)
clusters = model.transform(device_profiles_df)
```

**Deliverables:**
- `notebooks/03_fedhome_spark_clustering.ipynb`
- Clustering visualization figures
- Cluster assignment report

---

### Phase 4: Cluster-Aware Federated Training (Priority: MEDIUM)

**Tasks:**
- [ ] Group clients by cluster assignment
- [ ] Run FedMSE independently per cluster
- [ ] Track per-cluster metrics
- [ ] Compare cluster-specific vs. global models

**Training Loop:**
```python
for cluster_id in range(k_clusters):
    cluster_clients = get_clients_for_cluster(cluster_id)
    run_fedmse_training(cluster_clients, cluster_id)
```

**Deliverables:**
- Per-cluster training logs
- Cluster model comparison

---

### Phase 5: Ensemble Merge & Final Evaluation (Priority: MEDIUM)

**Tasks:**
- [ ] Implement weighted ensemble merge
- [ ] Evaluate final model on test set
- [ ] Compare FedHome vs. FedMSE baseline
- [ ] Generate all result figures

**Ensemble Method:**
```python
# Weighted average based on cluster size
final_weights = sum(cluster_size[i] * cluster_model[i] for i in range(k))
```

**Deliverables:**
- Final AUC comparison table
- All publication-ready figures
- Summary report

---

## 📁 File Organization

```
FedHome_Spark/
├── README.md                 # Project overview
├── PLAN.md                   # This file
├── baseline/                 # FedMSE baseline (cloned)
│   ├── src/
│   ├── Data/                 # Link to prepared dataset
│   └── ...
├── notebooks/
│   ├── 01_spark_setup.ipynb           # Phase 0
│   ├── 02_fedmse_spark_fullscale.ipynb # Phase 2
│   └── 03_fedhome_spark_clustering.ipynb # Phase 3
├── outputs/
│   ├── figures/
│   │   ├── device_type_distribution_matrix.png
│   │   ├── js_divergence_heatmap.png
│   │   ├── ward_dendrogram.png
│   │   ├── cluster_profiles.png
│   │   ├── auc_convergence_fedmse.png
│   │   ├── auc_convergence_fedhome.png
│   │   └── client_auc_comparison.png
│   ├── results/
│   │   ├── fedmse_baseline.json
│   │   └── fedhome_spark.json
│   └── logs/
├── spark_env/
│   └── spark_config.py
└── Knowledge_Base/
    ├── Context.md
    └── Initial_Plan.md
```

---

## ⏱️ Timeline

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 0 | Spark setup | 30 min |
| Phase 1 | FedMSE baseline | 2-3 hours (training) |
| Phase 2 | Spark data processing | 1-2 hours |
| Phase 3 | FedHome clustering | 1-2 hours |
| Phase 4 | Cluster-aware training | 2-3 hours (training) |
| Phase 5 | Final evaluation | 1 hour |
| **Total** | | **6-10 hours** |

---

## 📊 Success Criteria

| Criterion | Target |
|-----------|--------|
| FedMSE Baseline AUC | ≥0.97 |
| FedHome AUC Improvement | +1-2% over baseline |
| Spark Processing Speedup | 2x+ vs. pandas |
| Clustering Quality | Clear cluster separation |
| Full-Scale Completion | 50 clients, 20 rounds |

---

## 🔧 Technical Notes

### Spark Configuration (Local Mode)
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("FedHome") \
    .master("local[*]") \
    .config("spark.driver.memory", "16g") \
    .config("spark.executor.memory", "8g") \
    .config("spark.sql.shuffle.partitions", "10") \
    .getOrCreate()
```

### Memory Management
- MacBook Pro M5: 24GB RAM
- Allocate 16GB to Spark driver
- Use 10 partitions for 50 clients
- Monitor memory with Spark UI (localhost:4040)

---

## 📝 Notes for Presentation

- Emphasize **Apache Spark** as the distributed computing framework
- Mention **Spark MLlib** for clustering
- Focus on **scalability** and **big data processing** capabilities
- Architecture diagram shows Spark integration clearly

---

**Last Updated:** 2026-10-07  
**Status:** Ready to begin Phase 0
