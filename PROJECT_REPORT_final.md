# FedHome Project: Detailed Technical Report

**Project Title:** Device-Type-Aware Client Clustering for Privacy-Preserving Federated Anomaly Detection in Non-IID Smart Home IoT Networks

**Student:** Md. Raihan Sobhan  
**Course:** Big Data Analytics  
**Date:** August 2026  
**Status:** core project complete - Phases 0-5 executed with deterministic baseline and final ensemble evaluation on Saturday, August 8, 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Introduction and Motivation](#2-introduction-and-motivation)
3. [Problem Statement](#3-problem-statement)
4. [Background: FedMSE Baseline](#4-background-fedmse-baseline)
5. [FedHome Proposed Methodology](#5-fedhome-proposed-methodology)
6. [Implementation Details](#6-implementation-details)
7. [Experimental Setup](#7-experimental-setup)
8. [Results and Analysis](#8-results-and-analysis)
9. [Final Project Status and Scholarly Extensions](#9-final-project-status-and-scholarly-extensions)
10. [Working Directory Structure](#10-working-directory-structure)
11. [References](#11-references)

---

## 1. Executive Summary

This report documents the completed implementation and evaluation of **FedHome**, a federated anomaly detection framework for smart-home IoT botnet detection under high Non-IID conditions. FedHome extends the existing FedMSE baseline (Nguyen & Beuran, 2025) by introducing a **device-type-aware clustering layer** that groups IoT gateways by traffic-profile similarity before running specialized federated learning within each cluster and merging the resulting models into a global ensemble.

The final experimental pipeline was executed on **Saturday, August 8, 2026** using a deterministic split manifest. This is important because the original historical baseline run did not preserve row-level split indices. The deterministic rerun established a reproducible comparison baseline and enabled a strict apples-to-apples evaluation of the cluster-aware FedHome pipeline.

### Key Achievements

| Milestone | Status | Details |
|-----------|--------|---------|
| FedMSE Baseline Reproduction | ✅ Complete | Deterministic rerun on 50 clients, Non-IID (JS=0.83) |
| Deterministic Baseline Average AUC | ✅ 0.970844 | Authoritative baseline for all final comparisons |
| Deterministic Baseline Loss Reduction | ✅ 40.3% | `1.3442 -> 0.8030` over 20 rounds |
| Spark Data Pipeline | ✅ Complete | 136,565 rows processed across 50 gateways |
| Device-Type Clustering | ✅ Complete | Ward clustering with `C=2`, sizes `19/31`, silhouette `0.3967` |
| Phase 4 Cluster Training | ✅ Complete | Cluster 1 AUC `0.987283`, Cluster 2 AUC `0.967393` |
| Phase 5 Ensemble Evaluation | ✅ Complete | Global ensemble AUC `0.993082`, outperforming baseline |
| Reproducibility Infrastructure | ✅ Complete | Deterministic split manifest, saved metadata, and rerunnable scripts |

### Project Status Summary

- **Phase 0 (Environment Setup):** COMPLETE
- **Phase 1 (Baseline Reproduction):** COMPLETE
- **Phase 2 (Spark Data Processing):** COMPLETE
- **Phase 3 (Device Clustering):** COMPLETE
- **Phase 4 (Cluster-Aware FL Implementation):** COMPLETE
- **Phase 5 (Ensemble + Final Evaluation):** COMPLETE

---

## 2. Introduction and Motivation

### 2.1 The IoT Security Challenge

The proliferation of Internet of Things (IoT) devices in smart homes has created unprecedented security vulnerabilities. According to industry reports:

- **~21.9 billion** connected IoT devices worldwide by 2026 (Wireless Logic)
- **83%** of home Wi-Fi routers have firmware vulnerabilities (American Consumer Institute)
- **~1 million** compromised IoT devices reported in botnet networks (swif.ai)
- **Novel ("0-day+") attack variants** not present in labeled datasets are common (ENISA 2023)

### 2.2 Why Federated Learning?

Traditional centralized machine learning for botnet detection faces critical challenges:

1. **Privacy Concerns:** Raw network traffic data reveals occupancy patterns, health routines, and device usage behavior—information homeowners cannot share.
2. **Regulatory Compliance:** GDPR, CCPA, and other privacy regulations prohibit centralizing sensitive user data.
3. **Bandwidth Costs:** Transmitting all IoT traffic to a central server is prohibitively expensive.

**Federated Learning (FL)** addresses these challenges by:
- Training models locally on each gateway
- Sharing only model weights (not raw data)
- Aggregating weights into a global model

### 2.3 The Non-IID Challenge

Smart home IoT networks are inherently **Non-IID** (Non-Independent and Identically Distributed):

| Gateway | Device Composition | Traffic Pattern |
|---------|-------------------|-----------------|
| Home A | 4 cameras, 1 doorbell | High bandwidth, video streams |
| Home B | 2 thermostats, 5 smart bulbs | Low bandwidth, periodic updates |
| Home C | 1 baby monitor, 2 locks | Medium bandwidth, event-driven |

This heterogeneity creates a fundamental challenge: **a camera-heavy gateway and a thermostat-heavy gateway have completely different traffic distributions**. Standard federated averaging (FedAvg) produces a poor global model that fits neither well.

### 2.4 FedHome's Innovation

FedHome addresses the Non-IID challenge by:

1. **Clustering gateways** by their device-type composition (privacy-safe metadata)
2. **Running specialized FL** within each cluster
3. **Merging cluster models** via weighted ensemble

This produces **per-cluster specialized models** that handle Non-IID data more effectively than a single global model.

---

## 3. Problem Statement

### 3.1 Formal Problem Definition

**Given:**
- A set of $N$ smart home gateways $\{G_1, G_2, ..., G_N\}$
- Each gateway $G_i$ manages a heterogeneous mix of IoT devices
- Device-type distribution vector: $d_i = [p_1, p_2, ..., p_k]$ where $p_k$ = proportion of traffic from device class $k$
- Each gateway has local network traffic data $X_i$ (cannot leave the gateway)
- Data distributions are Non-IID across gateways (JS divergence = 0.83)

**Goal:**
Produce a set of cluster-specialized anomaly detection models $\{M^1, M^2, ..., M^C\}$ plus an ensemble merge $M_{global}$, such that:

1. **Privacy is preserved:** No raw traffic data $X_i$ leaves any gateway
2. **Non-IID is handled:** Models are specialized for different device-type clusters
3. **Detection accuracy is maximized:** AUC ≥ 97.3% on Mirai/Gafgyt botnet detection

### 3.2 Core Challenges

| Challenge ID | Challenge | Description | Impact |
|--------------|-----------|-------------|--------|
| C1 | Extreme Non-IID Data | Camera-heavy vs. thermostat-heavy gateways have totally different traffic distributions | Standard FedAvg produces poor global models |
| C2 | Label Scarcity | Attack traffic is rare and unlabeled in production; only normal traffic can be collected at scale | Detection must be semi-supervised/one-class |
| C3 | Device-Type Blindness | Existing FL approaches treat all gateways as equivalent clients, ignoring structural differences | Misses key signal for clustering |
| C4 | Privacy Constraint | Raw packet data cannot leave the gateway | Only model weights or abstracted statistics may be shared |

### 3.3 Threat Model

FedHome targets **Mirai** and **Gafgyt** botnet variants, which:
- Scan for vulnerable IoT devices
- Exploit default credentials
- Launch DDoS attacks from compromised device fleets

**Detection Approach:** Semi-supervised anomaly detection
- Train on **normal traffic only** (one-class learning)
- Detect deviations from learned normal patterns
- No labeled attack data required during training

---

## 4. Background: FedMSE Baseline

### 4.1 FedMSE Overview

**Citation:** Nguyen, V.T., & Beuran, R. (2025). *FedMSE: Semi-supervised federated learning approach for IoT network intrusion detection.* Computers & Security, 151, 104337.

FedMSE combines two innovations:

1. **SAE-CEN:** A local anomaly detector (Shrink Autoencoder + Centroid detector)
2. **MSEAvg:** A quality-aware aggregation algorithm (replaces FedAvg)

### 4.2 SAE-CEN: The Local Model

#### Shrink Autoencoder (SAE)

Standard Autoencoder loss:
$$L_{AE} = \frac{1}{n}\sum_{i=1}^{n}\|x_i - \hat{x}_i\|^2$$

SAE adds **latent shrinkage regularization**:
$$L_{SAE} = \frac{1}{n}\sum_{i=1}^{n}\|x_i - \hat{x}_i\|^2 + \lambda\cdot\frac{1}{n}\sum_{i=1}^{n}\|h_i\|^2$$

Where:
- $x_i$ = input sample
- $\hat{x}_i$ = reconstructed output
- $h_i$ = latent representation
- $\lambda$ = shrinkage regularization strength (hyperparameter)

**Effect:** The shrinkage term pulls the latent representations of "normal" data toward the origin, creating a **compact, dense cluster** in latent space. This makes it easier for a simple detector to separate normal from anomalous data.

#### Architecture Specifications

| Layer | Type | Dimensions | Activation |
|-------|------|------------|------------|
| Input | Raw features | 115 | - |
| Encoder 1 | Dense | 115 → 50 | ReLU |
| Encoder 2 | Dense | 50 → 11 | ReLU (latent) |
| Decoder 1 | Dense | 11 → 50 | ReLU |
| Decoder 2 | Dense | 50 → 115 | Sigmoid |
| Output | Reconstruction | 115 | - |

#### Centroid (CEN) Detector

After SAE training:
1. Compute centroid of normal data in latent space: $c = \frac{1}{n}\sum h_i$
2. For new sample $x$, compute anomaly score: $score(x) = \|encoder(x) - c\|_2$
3. Apply threshold: $score(x) > \tau \Rightarrow$ anomaly

**Advantages:**
- No hyperparameters
- Negligible compute cost
- Works with one-class (normal-only) training

### 4.3 MSEAvg: Quality-Aware Aggregation

#### The Problem with FedAvg

Standard FedAvg weights clients by **dataset size**:
$$W_{global} = \frac{\sum_{i=1}^{N} n_i \cdot W_i}{\sum_{i=1}^{N} n_i}$$

**Issue:** In Non-IID settings, a gateway with lots of data isn't necessarily representative of the whole network. A camera-heavy gateway with 10GB of data shouldn't dominate the model for thermostat gateways.

#### MSEAvg Solution

MSEAvg weights clients by **model quality** (reconstruction error on a shared development set):

**Algorithm:**
1. Server holds small development dataset $D_{dev}$ (normal data only, privacy-safe)
2. After each round, each local model $L_i$ reconstructs $D_{dev}$, producing $\hat{D}_i$
3. Compute $MSE_i = MSE(D_{dev}, \hat{D}_i)$ for each model
4. Assign weight $\alpha_i = 1 / MSE_i$ (better reconstruction → higher weight)
5. Global update: $W_{global} = \frac{\sum \alpha_i W_i}{\sum \alpha_i}$

**Key Insight:** MSEAvg is **quality-aware**, not size-aware. It's specifically designed to be robust to Non-IID heterogeneity.

### 4.4 FedMSE Reported Results

| Scenario | Gateways | Non-IID (JS) | FedAvg | FedMSE (SAE-CEN + MSEAvg) |
|----------|----------|--------------|--------|---------------------------|
| IID | 10 | ~0.01 | 99.0% | 99.3% |
| Non-IID | 10 | 0.83 | 93.98% ± 2.90 | **97.30% ± 0.49** |
| Non-IID | 50 | 0.83 | 91.5% | ~96% (extrapolated) |

**Key Observation:** FedMSE improves accuracy by **3.32%** and reduces variance by **6x** in high Non-IID settings.

---

## 5. FedHome Proposed Methodology

### 5.1 FedHome Overview

FedHome extends FedMSE by adding a **device-type-aware clustering layer** before federation:

| Aspect | FedMSE | FedHome (Proposed) |
|--------|--------|-------------------|
| Gateway Selection | Random | Cluster-aware |
| Model Specialization | Single global model | Per-cluster specialized models |
| Device-Type Signal | Ignored | Used for clustering |
| Non-IID Robustness | Moderate | High (by design) |

### 5.2 FedHome 4-Phase Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FedHome Architecture                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1: Device-Type Profiling                                  │
│  d_i = [p_1, ..., p_k]  (proportion per device class)           │
│                          │                                       │
│                          ▼                                       │
│  Phase 2: JS-Divergence Clustering                               │
│  D[i,j] = JS(d_i || d_j)  →  Ward hierarchical clustering       │
│                          │                                       │
│                          ▼                                       │
│  Phase 3: Cluster-Aware FL                                       │
│  Run FedMSE per cluster → M^c per cluster                        │
│                          │                                       │
│                          ▼                                       │
│  Phase 4: Ensemble Merge                                         │
│  M_global = Σ w^c · M^c  where w^c ∝ 1/MSE(M^c, D_dev)          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 Phase 1: Device-Type Profiling

**Input:** Each gateway $G_i$ reports device-type distribution vector:
$$d_i = [p_1, p_2, ..., p_k]$$

Where $p_k$ = proportion of traffic from device class $k$.

**N-BaIoT Device Types (9 classes):**
1. Danmini Doorbell
2. Ecobee Thermostat
3. Philips Baby Monitor
4. Provision PT-737E Security Camera
5. Provision PT-838 Security Camera
6. Samsung SNH-1011-N Webcam
7. SimpleHome XCS7-1002 Security Camera
8. SimpleHome XCS7-1003 Security Camera
9. Ennio Doorbell

**Example Gateway Profiles:**

| Gateway | Cameras | Doorbells | Thermostats | Baby Monitors |
|---------|---------|-----------|-------------|---------------|
| G1 | 0.70 | 0.20 | 0.05 | 0.05 |
| G2 | 0.10 | 0.10 | 0.70 | 0.10 |
| G3 | 0.05 | 0.05 | 0.10 | 0.80 |

**Privacy Guarantee:** Only device-type proportions are shared—no raw traffic data, no traffic content, no timestamps.

### 5.4 Phase 2: JS-Divergence Clustering

**Step 1: Compute Pairwise Distances**

Jensen-Shannon divergence between gateway profiles:
$$D[i,j] = JS(d_i \| d_j) = \frac{1}{2}KL(d_i \| m) + \frac{1}{2}KL(d_j \| m)$$

Where $m = \frac{1}{2}(d_i + d_j)$ and $KL$ is Kullback-Leibler divergence.

**Properties:**
- Symmetric: $JS(d_i \| d_j) = JS(d_j \| d_i)$
- Bounded: $0 \leq JS \leq 1$
- Interpretability: 0 = identical distributions, 1 = completely different

**Step 2: Ward Hierarchical Clustering**

Apply Ward's method to the distance matrix:
- Start with each gateway as its own cluster
- Iteratively merge closest clusters
- Minimize within-cluster variance at each step

**Output:** $C$ clusters of gateways with similar device-type mixes.

### 5.5 Phase 3: Cluster-Aware Federated Training

**For each cluster $c$:**
1. Initialize cluster model $M^c$ (SAE-CEN architecture)
2. Run FedMSE rounds within cluster:
   - Select 50% of cluster clients per round
   - Local training with SAE-CEN (100 epochs, lr=1e-5)
   - MSEAvg aggregation within cluster
3. Produce specialized cluster model $M^c$

**Key Advantage:** Each cluster model is specialized for its device-type composition, avoiding the "one-size-fits-all" problem of standard FL.

### 5.6 Phase 4: Ensemble Merge

The implemented ensemble is a **cluster-size-weighted parameter average** over the final cluster models:
$$W_{global} = \sum_{c=1}^{C} w^c \cdot W^c$$

where:
$$w^c = \frac{|C_c|}{\sum_{j=1}^{C}|C_j|}$$

For the final run:
- Cluster 1 weight = `19/50 = 0.38`
- Cluster 2 weight = `31/50 = 0.62`

**Intuition:** the final global model preserves cluster specialization while respecting the actual client mass represented by each cluster.

### 5.7 Research Questions

| RQ | Question | Evaluation Method |
|----|----------|-------------------|
| RQ1 | Does device-type-aware clustering improve AUC over FedMSE on high Non-IID networks (JS=0.83)? | Compare FedHome vs. FedMSE AUC on 50-gateway Non-IID scenario |
| RQ2 | What clustering granularity $k$ optimizes accuracy/overhead trade-off? | Evaluate $k \in \{3, 5, 7, 10\}$ clusters |
| RQ3 | How does FedHome scale from 10 to 50 gateways vs. FedMSE baseline? | Compare scaling curves (AUC vs. gateway count) |
| RQ4 | What is the communication overhead of cluster-ensemble vs. single-model? | Measure total bytes transmitted for convergence |

### 5.8 Achieved Outcomes

| Metric | Deterministic FedMSE Baseline | Achieved FedHome Outcome |
|--------|-----------------|----------------|
| Average AUC | `0.970844` | `0.993082` |
| Cluster 1 AUC | N/A | `0.987283` |
| Cluster 2 AUC | N/A | `0.967393` |
| AUC Delta | baseline | `+0.022238` |
| Convergence Rounds | `20` | `20` per cluster |
| Communication Structure | single global training | two cluster trainings + one merge |

---

## 6. Implementation Details

### 6.1 Technology Stack

| Component | Technology | Role in This Project |
|-----------|------------|----------------------|
| Federated anomaly detector | PyTorch + FedMSE baseline code | SAE-CEN training and MSEAvg aggregation |
| Data engineering | pandas + NumPy | deterministic split construction and result summarization |
| Distributed data processing | Apache Spark 3.5 | Phase 2 feature/statistics pipeline |
| Clustering and metrics | SciPy + scikit-learn + Spark MLlib | JS-distance analysis, Ward clustering, agreement checks |
| Visualization | Matplotlib + Seaborn | publication-style figures |
| Experiment control | Python scripts + JSON manifests | reproducible pipeline execution |

### 6.2 Final Runtime Configuration

| Parameter | Value |
|-----------|-------|
| Dataset scenario | N-BaIoT, 50-gateway non-IID split |
| Feature dimension | 115 |
| Global rounds | 20 |
| Local epochs | 100 |
| Client participation ratio | 0.5 |
| Learning rate | 1e-5 |
| Shrink lambda | 10 |
| Batch size | 12 |
| Spark mode | `local[*]` |
| Random seed | 42 |

### 6.3 Reproducibility Correction

The original baseline path used stochastic row shuffling without a persisted split manifest. To make the baseline scientifically comparable with later FedHome phases, a deterministic split system was introduced. The revised implementation now fixes client-level row ordering, train/validation/development/test indices, abnormal-data permutations, and development-set sampling. The resulting manifest is stored at `results/data/split_manifests/fedmse_fullscale_seed42.json` and is the authoritative reference for all final comparisons reported here.

### 6.4 Principal Modules Added for This Work

| File | Purpose |
|------|---------|
| `src/fedhome/split_manifest.py` | deterministic split generation, persistence, and replay |
| `src/fedhome/spark_data.py` | Spark-based Phase 2 pipeline and profile construction |
| `src/fedhome/clustering.py` | JS-divergence matrix construction and Phase 3 clustering |
| `src/fedhome/cluster_training.py` | cluster-wise federated training for Phase 4 |
| `src/fedhome/ensemble.py` | cluster-size-weighted ensemble merge and evaluation |
| `scripts/run_fedmse_baseline.py` | deterministic FedMSE baseline rerun |
| `scripts/run_phase2_spark_data.py` | Phase 2 driver |
| `scripts/run_phase3_clustering.py` | Phase 3 driver |
| `scripts/run_phase4_cluster_training.py` | Phase 4 driver |
| `scripts/run_phase5_ensemble.py` | Phase 5 driver |

### 6.5 High-Level Code Interfaces

The following interfaces capture the logic written for the completed pipeline. Only signatures and behavioral summaries are shown here, because the goal of this section is architectural understanding rather than line-by-line algorithm exposition.

#### 6.5.1 Deterministic Split Manifest

```python
def compute_split_sizes(total_rows: int) -> SplitSizes
def deterministic_permutation(size: int, seed: int) -> list[int]
def build_client_split_entry(
    device_name: str,
    normal_rows: int,
    abnormal_rows: int,
    new_normal_rows: int,
    shuffle_seed: int,
    dev_sample_seed: int,
) -> dict[str, Any]
def sample_dev_indices(dev_indices: list[int], target_size: int, seed: int) -> list[int]
def build_manifest(
    experiment_name: str,
    config_path: str,
    data_path: str,
    seed: int,
    client_entries: list[dict[str, Any]],
) -> dict[str, Any]
def save_manifest(manifest: dict[str, Any], path: Path) -> None
def load_manifest(path: Path) -> dict[str, Any]
```

These functions create and reuse a split manifest that records how each gateway dataset is partitioned, ensuring exact replay of the same experimental data boundary conditions.

#### 6.5.2 Phase 2: Spark Data Pipeline

```python
def create_spark_session(config: Phase2Config) -> SparkSession
def list_client_csvs(data_root: Path) -> List[Path]
def load_all_client_csvs(spark: SparkSession, data_root: Path) -> DataFrame
def compute_spark_split_counts(df: DataFrame) -> pd.DataFrame
def compute_spark_feature_stats(df: DataFrame, n_features: int = 115) -> pd.DataFrame
def reconstruct_profiles_from_counts(split_counts: pd.DataFrame) -> Tuple[pd.DataFrame, str]
def compute_profiles_from_feature_archetypes(...) -> Tuple[pd.DataFrame, str]
def write_profiles(
    output_dir: Path,
    profiles: pd.DataFrame,
    metadata: Dict[str, object],
) -> Tuple[Path, Path]
def run_phase2(config: Phase2Config) -> Dict[str, object]
```

This module ingests all gateway CSV files, computes Spark-side statistics, and produces the normalized 50x9 device-profile matrix used as the basis for clustering.

#### 6.5.3 Phase 3: Clustering and Visualization

```python
def load_profiles(path: Path) -> Tuple[List[str], np.ndarray, Dict[str, object]]
def js_distance_matrix(profiles: np.ndarray, epsilon: float = 1e-12) -> np.ndarray
def ward_labels(matrix: np.ndarray, c: int) -> Tuple[np.ndarray, np.ndarray]
def enforce_min_cluster_size(
    labels: np.ndarray,
    matrix: np.ndarray,
    min_size: int,
) -> Tuple[np.ndarray, List[Dict[str, int]]]
def evaluate_labels(matrix: np.ndarray, labels: np.ndarray) -> Dict[str, object]
def sweep_c(...) -> Tuple[List[Dict[str, object]], np.ndarray, np.ndarray, List[Dict[str, int]], int]
def spark_bisecting_kmeans_labels(...) -> np.ndarray
def plot_figures(...) -> Dict[str, Path]
def run_phase3(config: ClusteringConfig) -> Dict[str, object]
```

This phase computes pairwise Jensen-Shannon distances, selects the preferred number of clusters, produces diagnostic figures, and records cross-method agreement with Spark Bisecting K-Means.

#### 6.5.4 Phase 4: Cluster-Aware Federated Training

```python
def load_cluster_members(
    assignments_path: Path,
    manifest: dict[str, Any],
) -> dict[int, list[dict[str, Any]]]
def prepare_client_data(..., selected_client_entries: list[dict[str, Any]], batch_size: int) -> list[dict[str, Any]]
def build_global_dev_dataset(client_info: list[dict[str, Any]]) -> np.ndarray
def train_single_cluster(
    repo_root: Path,
    cluster_id: int,
    client_info: list[dict[str, Any]],
    config: ClusterRunConfig,
) -> tuple[dict[str, Any], dict[str, Any]]
def run_phase4(config: ClusterRunConfig) -> dict[str, Any]
```

The Phase 4 implementation partitions clients by cluster assignment, reuses the deterministic manifest, and trains one federated model per cluster using the same FedMSE mechanics as the baseline.

#### 6.5.5 Phase 5: Ensemble Merge and Final Evaluation

```python
def load_phase4_summary(path: Path) -> dict[str, Any]
def build_model() -> Shrink_Autoencoder
def weighted_average_state_dicts(
    weighted_models: list[tuple[dict[str, torch.Tensor], float]],
) -> dict[str, torch.Tensor]
def evaluate_global_ensemble(config: EnsembleConfig) -> dict[str, Any]
```

The ensemble stage merges cluster-level model parameters using cluster-size weights and then evaluates the merged model globally across all gateways.

---

## 7. Experimental Setup

### 7.1 Dataset: N-BaIoT

| Attribute | Value |
|-----------|-------|
| **Source** | Meidan et al. (2018) |
| **Devices** | 9 commercial IoT devices |
| **Device Types** | Cameras, Doorbells, Thermostats, Baby Monitors |
| **Attacks** | Mirai + Gafgyt botnet variants |
| **Features** | 115 network traffic features |
| **Scenarios** | IID and Non-IID distributions |

### 7.2 Non-IID Scenario (50 Clients)

| Parameter | Value |
|-----------|-------|
| **Distribution** | Dirichlet-based allocation |
| **JS Divergence** | 0.83 (high heterogeneity) |
| **Challenge** | Each gateway has different device-type mix |

### 7.3 Training Configuration

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Global Rounds | 20 | Standard FL convergence point |
| Local Epochs | 100 | FedMSE recommended default |
| Participant Ratio | 50% | Reduces communication cost |
| Learning Rate | 1e-5 | Optimal for SAE-CEN |
| Shrink Lambda ($\lambda$) | 10 | FedMSE recommended value |
| Batch Size | 12 | Memory-efficient on edge devices |
| Model | SAE-CEN + MSEAvg | FedMSE best performer |

### 7.4 Hardware

| Component | Specification |
|-----------|---------------|
| Platform | MacBook Pro M5 |
| RAM | 24GB |
| Spark Mode | Local[*] with 16GB driver memory |
| Training Time | ~3 minutes for 20 rounds |

---

## 8. Results and Analysis

### 8.1 Phase 1 Baseline: Deterministic FedMSE Rerun

The final baseline comparison is the deterministic rerun executed on Saturday, August 8, 2026 using the saved split manifest. This supersedes the earlier non-manifest run because it preserves exact train/validation/development/test boundaries for future replay.

| Metric | Deterministic Baseline |
|--------|------------------------|
| Average AUC | **0.970844** |
| Final loss | **0.8030** |
| Loss reduction | **40.3%** |
| Training time | **2.9 minutes** |
| Clients completed | **50 / 50** |

The baseline remained strong even after introducing strict reproducibility controls, establishing a defensible reference point for FedHome.

### 8.2 Phase 2: Spark Data Processing Outcomes

| Metric | Value |
|--------|-------|
| Gateways processed | 50 |
| Total rows processed | 136,565 |
| Output profile matrix | 50 x 9 |
| Row-normalization check | all rows sum to 1.0 +/- 1e-6 |
| Spark runtime | 17.03 s |
| pandas runtime | 1.12 s |

Phase 2 successfully produced the normalized profile matrix used in downstream clustering. A technically important caveat is that the scenario files do not carry explicit row-level device labels; therefore the saved profiles are traffic-archetype proxies rather than direct device-identity distributions. This limitation should be stated transparently in any scholarly presentation of the method.

### 8.3 Phase 3: Clustering Results

| Metric | Value |
|--------|-------|
| Distance metric | Jensen-Shannon divergence |
| Primary clustering method | Ward hierarchical clustering |
| Selected cluster count | 2 |
| Cluster sizes | 19, 31 |
| Silhouette score | 0.3967 |
| Ward vs Spark BKM ARI | 0.6998 |

The resulting partition shows interpretable heterogeneity, but the silhouette score is below the aspirational `> 0.5` target. Given the proxy nature of the phase-2 profiles, the clustering should be interpreted as an operationally useful grouping rather than a perfect latent device taxonomy.

### 8.4 Phase 4: Cluster-Aware Federated Training

| Cluster | Clients | Average AUC | Final Loss | Minimum AUC | Maximum AUC | Training Time (s) |
|---------|---------|-------------|------------|-------------|-------------|-------------------|
| 1 | 19 | **0.987283** | 0.815616 | 0.952492 | 0.999997 | 120.47 |
| 2 | 31 | **0.967393** | 0.862165 | 0.621677 | 1.000000 | 122.05 |

Cluster 1 achieved the stronger mean discrimination performance, while Cluster 2 displayed a broader spread in client difficulty. This asymmetry is consistent with the heterogeneity suggested by the Phase 3 cluster structure.

### 8.5 Phase 5: Ensemble Merge and Final Global Evaluation

| Metric | Value |
|--------|-------|
| Merge rule | cluster-size-weighted parameter average |
| Cluster weights | 19/50 and 31/50 |
| FedHome ensemble average AUC | **0.993082** |
| Ensemble minimum AUC | 0.898831 |
| Ensemble maximum AUC | 1.000000 |
| Baseline average AUC | 0.970844 |
| Absolute AUC improvement | **+0.022238** |

The final ensemble surpassed the deterministic baseline by approximately 2.22 AUC points, providing the central empirical result of the project: a cluster-aware federated workflow improved global anomaly-detection performance over the single-model FedMSE baseline under the same reproducible data split.

### 8.6 Comparative Interpretation

| Experiment | Average AUC | Final Loss | Notes |
|------------|-------------|------------|-------|
| FedMSE baseline | 0.970844 | 0.8030 | single global model |
| Phase 4 Cluster 1 | 0.987283 | 0.815616 | specialized model for 19 clients |
| Phase 4 Cluster 2 | 0.967393 | 0.862165 | specialized model for 31 clients |
| Phase 5 FedHome ensemble | **0.993082** | N/A | cluster-size-weighted merged model |

Taken together, the results support the project hypothesis that heterogeneity-aware grouping can yield a stronger global detector than a single homogeneous federated model, even when the grouping signal is derived from proxy traffic archetypes.

### 8.7 Output Artifacts

The final report is supported by the following authoritative result files:

- `results/data/fedmse_fullscale_20260808_153506.json`
- `results/data/fedmse_fullscale_20260808_153506_metadata.json`
- `results/data/split_manifests/fedmse_fullscale_seed42.json`
- `results/data/device_profiles.csv`
- `results/data/cluster_assignments.csv`
- `results/data/js_divergence_matrix.csv`
- `results/data/phase4_cluster_training_20260808_154251/phase4_cluster_training_summary.json`
- `results/data/phase4_cluster_training_20260808_154251/phase5_ensemble_summary.json`
- `results/figures/`

---

## 9. Final Project Status and Scholarly Extensions

### 9.1 Final Implementation Status

| Component | Status | Evidence |
|-----------|--------|----------|
| FedMSE deterministic baseline | Complete | manifest + rerun outputs |
| Phase 2 Spark data pipeline | Complete | profiles, split counts, feature summaries |
| Phase 3 clustering and visualization | Complete | assignments, JS matrix, diagnostic figures |
| Phase 4 cluster-aware federated training | Complete | cluster summaries and trained checkpoints |
| Phase 5 ensemble merge and evaluation | Complete | ensemble summary and saved model |
| Reporting and presentation assets | Complete | report, figures, tables, slide asset folder |

### 9.2 Completed Deliverables

| Deliverable | Location |
|-------------|----------|
| Deterministic baseline pipeline | `scripts/run_fedmse_baseline.py` |
| Split-manifest utility | `src/fedhome/split_manifest.py` |
| Spark profiling pipeline | `src/fedhome/spark_data.py` |
| Clustering engine | `src/fedhome/clustering.py` |
| Cluster-aware FL engine | `src/fedhome/cluster_training.py` |
| Ensemble merge engine | `src/fedhome/ensemble.py` |
| Final status note | `FINAL_RESULTS_20260808.md` |
| Slide and paper assets | `presentation/assets_20260808/` |

### 9.3 Suggested Scholarly Extensions

Although the implementation goals of this project are complete, three academically meaningful extensions remain natural next steps: first, replacing proxy archetype profiles with true row-level device labels where available; second, comparing against additional heterogeneity-aware federated baselines such as FedProx or IFCA; third, scaling the pipeline from local Spark execution to a multi-node deployment to test whether the engineering design continues to hold at larger operational scale.

---

## 10. Working Directory Structure

```text
FedHome_Spark/
├── README.md
├── FINAL_RESULTS_20260808.md
├── PROJECT_REPORT.md
├── baseline/
│   ├── Data/
│   ├── README.md
│   ├── requirements.txt
│   └── src/
├── experiments/
│   ├── 01_spark_setup.ipynb
│   ├── 01_spark_setup_simple.ipynb
│   ├── 02_fedmse_spark_fullscale.ipynb
│   └── 03_fedhome_spark_clustering.ipynb
├── scripts/
│   ├── run_fedmse_baseline.py
│   ├── run_phase2_spark_data.py
│   ├── run_phase3_clustering.py
│   ├── run_phase4_cluster_training.py
│   ├── run_phase5_ensemble.py
│   ├── generate_comparison_figures.py
│   ├── generate_figures.py
│   ├── run_test.sh
│   └── test_setup.py
├── src/
│   └── fedhome/
│       ├── __init__.py
│       ├── split_manifest.py
│       ├── spark_data.py
│       ├── clustering.py
│       ├── cluster_training.py
│       └── ensemble.py
├── results/
│   ├── EXPERIMENT_LOG.md
│   ├── data/
│   │   ├── device_profiles.csv
│   │   ├── cluster_assignments.csv
│   │   ├── js_divergence_matrix.csv
│   │   ├── fedmse_fullscale_20260808_153506.json
│   │   ├── fedmse_fullscale_20260808_153506_metadata.json
│   │   ├── spark_pandas_benchmark.json
│   │   ├── split_manifests/
│   │   └── phase4_cluster_training_20260808_154251/
│   ├── figures/
│   └── logs/
└── presentation/
    ├── presentation.tex
    ├── FedHome_Presentation_Slides.md
    ├── README_Overleaf.md
    ├── figures/
    └── assets_20260808/
        ├── figures/
        └── tables/
```

### 10.1 Slide and Paper Asset Folder

All reusable figure and table assets have been consolidated into `presentation/assets_20260808/` for presentation development and later paper writing.

**Figures copied to `presentation/assets_20260808/figures/`:**
- `auc_convergence_fullscale.png`
- `auc_distribution_histogram.png`
- `client_auc_distribution.png`
- `client_auc_heatmap.png`
- `js_distance_heatmap_ordered_phase3.png`
- `mds_clusters_phase3.png`
- `silhouette_vs_c_phase3.png`
- `training_time_per_round.png`
- `ward_dendrogram_phase3.png`

**Tables prepared in `presentation/assets_20260808/tables/`:**
- `baseline_final_summary.csv`
- `phase2_benchmark_summary.csv`
- `phase3_clustering_summary.csv`
- `phase4_cluster_summary.csv`
- `phase5_ensemble_summary.csv`
- `phase5_client_results.csv`
- `device_profiles.csv`
- `client_feature_stats_spark.csv`
- `client_split_counts_spark.csv`
- `cluster_assignments.csv`
- `js_divergence_matrix.csv`

---

## 11. References

1. Nguyen, V.T., & Beuran, R. (2025). FedMSE: Semi-supervised federated learning approach for IoT network intrusion detection. *Computers & Security*, 151, 104337.

2. Meidan, Y., Bohadana, M., Mathov, Y., Mirsky, Y., Shainin, A., & Elovici, Y. (2018). N-BaIoT: Network-based Detection of IoT Botnet Attacks Using Deep Autoencoders. *IEEE Pervasive Computing*, 17(3), 12-22.

3. McMahan, B., Moore, E., Ramage, D., Hampson, S., & Arcas, B.A.Y. (2017). Communication-Efficient Learning of Deep Networks from Decentralized Data. *AISTATS*.

4. Li, T., Sahu, A.K., Talwalkar, A., & Smith, V. (2020). Federated Learning: Challenges, Methods, and Future Directions. *IEEE Signal Processing Magazine*, 37(3), 50-60.

5. Apache Spark. (2026). Apache Spark 3.5 Documentation. https://spark.apache.org/

---

**Document Version:** 1.1  
**Last Updated:** August 8, 2026  
**Author:** Md. Raihan Sobhan  
**Course:** Big Data Analytics
