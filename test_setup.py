#!/usr/bin/env python
"""
FedHome_Spark - Quick Setup Test
Tests basic imports and data loading before running full notebooks
"""

import sys
import os
import json

# Change to baseline/src directory (where FedMSE expects to run from)
os.chdir('baseline/src')
sys.path.insert(0, '.')

print("="*60)
print("FEDHOME_SPARK SETUP TEST")
print("="*60)

# Test 1: Check configuration
print("\n[1/5] Checking configuration file...")
config_file = "Configuration/scen2-nba-iot-50clients.json"
with open(config_file, "r") as f:
    config = json.load(f)
print(f"  ✓ Config loaded: {config_file}")
print(f"  Data path: {config['data_path']}")
print(f"  Clients: {len(config['devices_list'])}")

# Test 2: Check data exists
print("\n[2/5] Checking data files...")
data_base = config['data_path']
client1_normal = os.path.join(data_base, "Client-1", "normal")
if os.path.isdir(client1_normal):
    print(f"  ✓ Data directory found: {client1_normal}")
else:
    print(f"  ✗ Data NOT found: {client1_normal}")
    sys.exit(1)

# Test 3: Test FedMSE imports
print("\n[3/5] Testing FedMSE imports...")
try:
    from Model import Shrink_Autoencoder
    from DataLoader import load_data
    print("  ✓ FedMSE modules imported")
except Exception as e:
    print(f"  ✗ Import error: {e}")
    sys.exit(1)

# Test 4: Test data loading
print("\n[4/5] Testing data loading...")
try:
    test_data = load_data(client1_normal)
    print(f"  ✓ Data loaded: {len(test_data)} rows, {len(test_data.columns)} columns")
except Exception as e:
    print(f"  ✗ Data load error: {e}")
    sys.exit(1)

# Test 5: Test PySpark
print("\n[5/5] Testing PySpark...")
try:
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName("Test").master("local[1]").config("spark.driver.memory", "4g").getOrCreate()
    df = spark.range(10)
    count = df.count()
    spark.stop()
    print(f"  ✓ PySpark working: test count = {count}")
except Exception as e:
    print(f"  ✗ PySpark error: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\nReady to run notebooks from FedHome_Spark directory:")
print("  1. notebooks/01_spark_setup_simple.ipynb")
print("  2. notebooks/02_fedmse_spark_fullscale.ipynb")
print("  3. notebooks/03_fedhome_spark_clustering.ipynb")
print("\nNOTE: Run notebooks from the FedHome_Spark root directory!")
