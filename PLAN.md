# FedHome_Spark Implementation Plan

**Project:** FedHome - Spark-Enhanced Federated Learning for IoT Botnet Detection  
**Student:** Md. Raihan Sobhan  
**Course:** Big Data Analytics  

**Last Updated:** 2026-10-07  
**Status:** ✅ Phase 1 Complete - Baseline Results Achieved

---

## 📋 Project Goals

1. **Reproduce FedMSE Baseline:** ✅ VALIDATED - Achieved 0.9829 AUC with 50 clients
2. **Implement FedHome with Spark:** 🔄 In Progress - Spark environment ready
3. **Full-Scale Evaluation:** ✅ COMPLETE - 50 clients, 20 rounds, 100 epochs
4. **Generate Publication-Ready Results:** ✅ COMPLETE - 3 figures generated

---

## 🎯 Implementation Phases

### Phase 0: Environment Setup ✅ COMPLETE

**Status:** All tasks completed successfully

**Completed Tasks:**
- [x] Install PySpark via pip
- [x] Verify Java installation (Spark requirement)
- [x] Create Spark session configuration
- [x] Test Spark with simple operations
- [x] Create test_setup.py script

**Deliverables:**
- ✅ `spark_env/` - Virtual environment configured
- ✅ `scripts/test_setup.py` - Setup verification script
- ✅ `experiments/01_spark_setup_simple.ipynb` - Spark setup notebook

---

### Phase 1: FedMSE Baseline Reproduction ✅ COMPLETE

**Status:** COMPLETED with excellent results

**Completed Tasks:**
- [x] Link prepared dataset to `baseline/Data/`
- [x] Run smoke test with 10 clients (verification)
- [x] Run full-scale with 50 clients
- [x] Generate baseline result figures

**Results Achieved:**
| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| Average AUC | ≥0.97 | **0.9829** | ✅ Exceeded |
| Loss Reduction | >30% | **41.0%** | ✅ Exceeded |
| Training Time | <5 min | **2.87 min** | ✅ Exceeded |

**Configuration Used:**
- Clients: 50 (Non-IID)
- Rounds: 20
- Local Epochs: 100
- Participant Ratio: 50%
- Model: SAE-CEN + MSEAvg

**Deliverables:**
- ✅ `results/data/fedmse_fullscale_20260710_214108.json` - Full results
- ✅ `results/figures/auc_convergence_fullscale.png` - AUC convergence
- ✅ `results/figures/client_auc_distribution.png` - Client distribution
- ✅ `results/figures/training_time_per_round.png` - Time analysis
- ✅ `results/logs/fedmse_run.log` - Training logs
- ✅ `models/fedmse_checkpoints/Client_*/` - 20 model checkpoints

---

### Phase 2: Spark-Enhanced Data Processing 🔄 READY

**Status:** Environment ready, implementation pending

**Tasks:**
- [x] Install PySpark
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
- `experiments/02_fedmse_spark_fullscale.ipynb` (ready to execute)
- Performance comparison (Spark vs. pandas)

---

### Phase 3: FedHome Spark Clustering 🔄 READY

**Status:** Environment ready, implementation pending

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
- `experiments/03_fedhome_spark_clustering.ipynb` (ready to execute)
- Clustering visualization figures
- Cluster assignment report

---

### Phase 4: Cluster-Aware Federated Training ⏳ PENDING

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

### Phase 5: Ensemble Merge & Final Evaluation ⏳ PENDING

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

## 📁 Current File Organization

```
FedHome_Spark/
├── README.md                 # ✅ UPDATED with results
├── PLAN.md                   # This file (UPDATED)
├── baseline/                 # FedMSE baseline (cloned)
│   ├── src/                 # FedMSE source code
│   └── Data/                # Dataset linked
├── experiments/              # ✅ Jupyter notebooks
│   ├── 01_spark_setup_simple.ipynb
│   ├── 02_fedmse_spark_fullscale.ipynb
│   └── 03_fedhome_spark_clustering.ipynb
├── scripts/                  # ✅ Python scripts
│   ├── run_fedmse_baseline.py
│   ├── generate_figures.py
│   └── test_setup.py
├── results/                  # ✅ Experiment outputs
│   ├── data/                # JSON results
│   ├── figures/             # Generated plots (300 DPI)
│   └── logs/                # Training logs
├── models/                   # ✅ Trained checkpoints
│   └── fedmse_checkpoints/  # 20 client models
├── Knowledge_Base/           # ✅ Documentation
│   ├── Context.md
│   └── Initial_Plan.md
└── spark_env/                # ✅ Virtual environment
```

---

## ⏱️ Updated Timeline

| Phase | Status | Time Spent | Notes |
|-------|--------|------------|-------|
| Phase 0 | ✅ Complete | 30 min | Spark setup done |
| Phase 1 | ✅ Complete | 3 min | Faster than expected! |
| Phase 2 | 🔄 Ready | - | Can execute anytime |
| Phase 3 | 🔄 Ready | - | Can execute anytime |
| Phase 4 | ⏳ Pending | - | After clustering |
| Phase 5 | ⏳ Pending | - | Final evaluation |
| **Total So Far** | | **~33 min** | Baseline complete |

---

## 📊 Success Criteria - Updated

| Criterion | Target | Current | Status |
|-----------|--------|---------|--------|
| FedMSE Baseline AUC | ≥0.97 | **0.9829** | ✅ Achieved |
| FedHome AUC Improvement | +1-2% | - | ⏳ Pending |
| Spark Processing Speedup | 2x+ | - | 🔄 Ready to test |
| Clustering Quality | >0.5 | - | 🔄 Ready to test |
| Full-Scale Completion | 50 clients | ✅ 50 clients | ✅ Complete |

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

## 📝 Next Steps

1. **Execute Spark Clustering** (`experiments/03_fedhome_spark_clustering.ipynb`)
2. **Run Cluster-Aware Training** (Phase 4)
3. **Generate Comparative Results** (FedHome vs. FedMSE)
4. **Prepare Final Presentation**

---

## 📝 Notes for Presentation

- ✅ Emphasize **Apache Spark** as the distributed computing framework
- ✅ Mention **Spark MLlib** for clustering
- ✅ Focus on **scalability** and **big data processing** capabilities
- ✅ Architecture diagram shows Spark integration clearly
- ✅ Baseline results validated (0.9829 AUC)

---

**Last Updated:** 2026-10-07  
**Status:** ✅ Phase 1 Complete | 🔄 Phase 2-3 Ready | ⏳ Phase 4-5 Pending
