# FedHome_Spark - Initial Project Plan

**Created:** 2026-10-07  
**Last Updated:** 2026-10-07  
**Student:** Md. Raihan Sobhan  
**Course:** Big Data Analytics

**Status:** ✅ Phase 1 Complete - Baseline Results Achieved

---

## 🚀 Project Initiation

This document outlines the initial plan for setting up and executing the FedHome_Spark project - a Spark-enhanced federated learning system for IoT botnet detection.

---

## 📋 Initial Setup Checklist

### 1. Directory Structure ✅ COMPLETE
```bash
FedHome_Spark/
├── baseline/        # FedMSE codebase
├── experiments/     # Jupyter notebooks
├── scripts/         # Python scripts
├── results/         # Experiment outputs
├── models/          # Model checkpoints
├── Knowledge_Base/  # Documentation
└── spark_env/       # Virtual environment
```
**Status:** ✅ Complete - Well organized structure

### 2. Clone Baseline Repository ✅ COMPLETE
```bash
git clone https://github.com/dino-chiio/fedmse.git baseline
```
**Status:** ✅ Complete - FedMSE baseline integrated

### 3. Create Documentation ✅ COMPLETE
- [x] README.md - Project overview (UPDATED with results)
- [x] PLAN.md - Implementation plan (UPDATED with progress)
- [x] Knowledge_Base/Context.md - Project context (UPDATED)
- [x] Knowledge_Base/Initial_Plan.md - This file (UPDATED)

### 4. Environment Setup ✅ COMPLETE
```bash
# Check Java (required for Spark)
java -version  # ✅ Verified

# Install PySpark
pip install pyspark pandas numpy torch scikit-learn matplotlib seaborn  # ✅ Done
```
**Status:** ✅ Complete - Spark ready

### 5. Dataset Setup ✅ COMPLETE
```bash
# Dataset linked and extracted
baseline/Data/Prepared_dataset.zip  # ✅ 50 clients, Non-IID
```
**Status:** ✅ Complete - 50 clients ready

---

## 🎯 Execution Plan - Progress Update

### Phase 0: Spark Environment Setup ✅ COMPLETE

**File:** `experiments/01_spark_setup_simple.ipynb`

**Status:** ✅ Complete

```python
from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("FedHome") \
    .master("local[*]") \
    .config("spark.driver.memory", "16g") \
    .config("spark.executor.memory", "8g") \
    .getOrCreate()

# Test basic operations
df = spark.range(1000)
print(f"Spark working! Count: {df.count()}")
```

**Expected Output:** ✅ Verified
- Spark session initialized
- Basic operations work
- Spark UI available at localhost:4040

---

### Phase 1: FedMSE Baseline Run ✅ COMPLETE

**File:** `scripts/run_fedmse_baseline.py`

**Status:** ✅ COMPLETE - Excellent results achieved!

**Configuration Used:**
- 50 clients (Non-IID)
- 20 global rounds
- 100 local epochs
- 50% participant ratio
- SAE-CEN + MSEAvg

**Results Achieved:**

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| Average AUC | ≥0.97 | **0.9829** | ✅ Exceeded |
| Min AUC | - | 0.8021 | ✅ Good |
| Max AUC | - | 1.0000 | ✅ Perfect |
| Loss Reduction | >30% | **41.0%** | ✅ Exceeded |
| Training Time | <5 min | **2.87 min** | ✅ Exceeded |

**Expected Runtime:** 2-3 hours → **Actual: 2.87 minutes!** (Much faster than expected)

**Generated Files:**
- ✅ `results/data/fedmse_fullscale_20260710_214108.json`
- ✅ `results/figures/auc_convergence_fullscale.png`
- ✅ `results/figures/client_auc_distribution.png`
- ✅ `results/figures/training_time_per_round.png`
- ✅ `results/logs/fedmse_run.log`
- ✅ `models/fedmse_checkpoints/Client_*/` (20 models)

---

### Phase 2: FedHome Spark Clustering 🔄 READY

**File:** `experiments/03_fedhome_spark_clustering.ipynb`

**Status:** 🔄 Ready to execute

```python
from pyspark.ml.clustering import BisectingKMeans
from pyspark.ml.feature import VectorAssembler

# Device-type profiles
device_profiles = [...]  # (n_gateways, n_device_classes)

# Clustering
bm = BisectingKMeans(k=5)
model = bm.fit(profiles_df)
clusters = model.transform(profiles_df)
```

**Expected Output:**
- 5 clusters identified
- Cluster assignment for each gateway
- Visualization of cluster profiles

---

### Phase 3: Final Evaluation ⏳ PENDING

**Files:** Results in `results/data/`

**Deliverables:**
1. ⏳ AUC convergence figures (FedMSE vs FedHome)
2. ✅ Client-wise AUC comparison (baseline done)
3. ⏳ Clustering visualization
4. ✅ Summary statistics JSON (baseline done)

---

## 📊 Expected vs. Actual Results

| Experiment | Clients | Rounds | Epochs | Expected AUC | Actual AUC | Status |
|------------|---------|--------|--------|--------------|------------|--------|
| FedMSE Baseline | 50 | 20 | 100 | ~0.97 | **0.9829** | ✅ Complete |
| FedHome (Spark) | 50 | 20 | 100 | ~0.98+ | - | 🔄 Pending |

---

## 🔧 Troubleshooting

### Common Issues - Resolved

**1. Java Not Found** ✅ Resolved
```bash
# Already installed on system
java -version  # Works
```

**2. Spark Memory Error** ✅ Prepared
```python
# Configured appropriately
.config("spark.driver.memory", "16g")
```

**3. Path Configuration** ✅ Fixed
```python
# Updated in scripts/run_fedmse_baseline.py
# Uses relative paths from scripts/ directory
```

---

## 📝 Current Project Status

### Completed ✅
1. Project structure setup
2. FedMSE baseline cloned and configured
3. Spark environment configured
4. Dataset prepared (50 clients, Non-IID)
5. FedMSE baseline run completed
6. Result figures generated (3 publication-ready figures)
7. Directory organized (scripts/, results/, models/, experiments/)
8. Documentation updated (README, PLAN, Context)

### Ready to Execute 🔄
1. Spark clustering notebook
2. Cluster-aware federated training
3. Ensemble merge and final evaluation

### Pending ⏳
1. FedHome full implementation
2. Comparative analysis (FedHome vs. FedMSE)
3. Final presentation preparation

---

## 📝 Notes

- ✅ This project uses Apache Spark for distributed computing
- ✅ All experiments run locally on MacBook Pro M5 (24GB RAM)
- ✅ Baseline results validated and exceeded expectations (0.9829 AUC)
- ✅ Training completed in under 3 minutes (much faster than expected)
- For presentation, we report "Apache Spark" as the distributed framework
- The focus is on demonstrating Spark integration for big data processing

---

## 📈 Key Achievements So Far

| Achievement | Details |
|-------------|---------|
| **Baseline AUC** | 0.9829 (exceeded 0.97 target) |
| **Loss Reduction** | 41.0% (1.37 → 0.81) |
| **Training Speed** | 2.87 minutes for 20 rounds |
| **All Clients** | 50/50 completed successfully |
| **Figures Generated** | 3 publication-ready plots |
| **Code Organized** | Clean directory structure |
| **Documentation** | All markdowns updated |

---

**Next Action:** Execute Spark clustering notebook (`experiments/03_fedhome_spark_clustering.ipynb`)

**Last Updated:** 2026-10-07  
**Status:** ✅ Phase 1 Complete | 🔄 Phase 2-3 Ready | ⏳ Phase 4-5 Pending
