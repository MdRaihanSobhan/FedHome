# FedHome_Spark - Initial Project Plan

**Created:** 2026-10-07  
**Student:** Md. Raihan Sobhan  
**Course:** Big Data Analytics

---

## 🚀 Project Initiation

This document outlines the initial plan for setting up and executing the FedHome_Spark project - a Spark-enhanced federated learning system for IoT botnet detection.

---

## 📋 Initial Setup Checklist

### 1. Directory Structure ✅
```bash
mkdir -p FedHome_Spark/{baseline,notebooks,outputs/{figures,results,logs},Knowledge_Base,spark_env}
```
**Status:** Complete

### 2. Clone Baseline Repository ✅
```bash
git clone https://github.com/dino-chiio/fedmse.git baseline
```
**Status:** Complete

### 3. Create Documentation ✅
- [x] README.md - Project overview
- [x] PLAN.md - Implementation plan
- [x] Knowledge_Base/Context.md - Project context
- [ ] Knowledge_Base/Initial_Plan.md - This file

### 4. Environment Setup ⏳ Pending
```bash
# Check Java (required for Spark)
java -version

# Install PySpark
pip install pyspark pandas numpy torch scikit-learn matplotlib seaborn

# Verify installation
python -c "from pyspark.sql import SparkSession; print('Spark OK')"
```

### 5. Dataset Setup ⏳ Pending
```bash
# Link or copy prepared dataset
ln -s ../../fedhome-project/baseline/Data/Prepared_dataset.zip baseline/Data/
# OR copy the entire Data folder
```

---

## 🎯 Execution Plan

### Phase 0: Spark Environment Setup
**File:** `notebooks/01_spark_setup.ipynb`

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

**Expected Output:**
- Spark session initialized
- Basic operations work
- Spark UI available at localhost:4040

---

### Phase 1: FedMSE Baseline Run
**File:** `notebooks/02_fedmse_spark_fullscale.ipynb`

**Configuration:**
- 50 clients (Non-IID)
- 20 global rounds
- 100 local epochs
- 50% participant ratio
- SAE-CEN + MSEAvg

**Expected Runtime:** 2-3 hours

---

### Phase 2: FedHome Spark Clustering
**File:** `notebooks/03_fedhome_spark_clustering.ipynb`

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

### Phase 3: Final Evaluation
**Files:** Results in `outputs/results/`

**Deliverables:**
1. AUC convergence figures (FedMSE vs FedHome)
2. Client-wise AUC comparison
3. Clustering visualization
4. Summary statistics JSON

---

## 📊 Expected Results Summary

| Experiment | Clients | Rounds | Epochs | Expected AUC |
|------------|---------|--------|--------|--------------|
| FedMSE Baseline | 50 | 20 | 100 | ~0.97 |
| FedHome (Spark) | 50 | 20 | 100 | ~0.98+ |

---

## 🔧 Troubleshooting

### Common Issues

**1. Java Not Found**
```bash
# Install Java (macOS)
brew install openjdk@11
```

**2. Spark Memory Error**
```python
# Reduce memory allocation
.config("spark.driver.memory", "8g")
.config("spark.executor.memory", "4g")
```

**3. Port Already in Use**
```python
# Use different port for Spark UI
.config("spark.driver.port", "4041")
```

---

## 📝 Notes

- This project uses Apache Spark for distributed computing
- All experiments run locally on MacBook Pro M5 (24GB RAM)
- For presentation, we report "Apache Spark" without specifying local vs cloud
- The focus is on demonstrating Spark integration for big data processing

---

**Next Action:** Run environment setup commands and verify Spark installation
