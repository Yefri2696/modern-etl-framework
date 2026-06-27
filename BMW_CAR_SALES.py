"""
Project: BMW Car Sales & Price Analysis
Author: Oscar Hernández

Objective:
- Load historical BMW car sales and price data.
- Clean and standardize raw columns.
- Assess data quality (missing values, duplicates, dtypes).
- Analyze how prices evolve over time.
- Export a clean dataset for dashboards and further modeling.

Pipeline:
Extract -> Inspect -> Clean -> Analyze -> Visualize -> Export
"""

# ============================
# 0. LIBRARIES AND MODULES
# ============================

from extract import extract
from transform import TransformPipeline, ColumnCleaner, TypeCaster

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd

# ============================
# 1. EXTRACT: LOAD RAW DATA
# ============================

# Load the dataset from a ZIP file (local path).
# In the GitHub README, explain where the data comes from
# and how someone else can download or reproduce it.
df_raw = extract(
    r'C:\Users\yefri\OneDrive\Escritorio\datos\Data\Dataset\BMW Car sales and Price Dataset.zip'
)

print("===== RAW DATA (first 10 rows) =====")
print(df_raw.head(10))

# ============================
# 2. DATA QUALITY CHECKS
# ============================

# Number of fully duplicated rows
num_duplicates = df_raw.duplicated().sum()
print(f"\nNumber of duplicated rows: {num_duplicates}")

# Missing values per column
print("\n===== Missing values per column =====")
print(df_raw.isnull().sum())

# Initial data types
print("\n===== Data types (raw) =====")
print(df_raw.dtypes)

# ============================
# 3. TRANSFORM: CLEANING & TYPES
# ============================

# Transformation pipeline:
# - ColumnCleaner: trims whitespace, standardizes column names
#   (e.g. lower case), and handles basic cleaning.
# - TypeCaster: converts 'year' to datetime for time-based analysis.
pipeline = TransformPipeline([
    ColumnCleaner(strip=True, lower=True),
    TypeCaster({'year': 'datetime'})
])

df = pipeline.run(df_raw)

print("\n===== DATA AFTER PIPELINE (first 10 rows) =====")
print(df.head(10))

print("\n===== Data types (post-pipeline) =====")
print(df.dtypes)


# ============================
# 4. BASIC ANALYSIS
# ============================

print("\n===== Descriptive statistics for price =====")
print(df['price'].describe())


# Price metrics by year
price_by_year_mean = df.groupby('year')['price'].mean()
price_by_year_sum = df.groupby('year')['price'].sum()

print("\n===== Average price by year =====")
print(price_by_year_mean)

print("\n===== Total price by year =====")
print(price_by_year_sum)

# ============================
# 5. VISUALIZATIONS
# ============================

plt.style.use("seaborn-v0_8-whitegrid")

# Annual summaries
avg_price_by_year = df.groupby('year', as_index=False)['price'].mean()
median_price_by_year = df.groupby('year', as_index=False)['price'].median()

# ----------------------------
# 5.1 Price over time
# ----------------------------
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    df['year'],
    df['price'],
    color='#1f4e79',
    linewidth=2.2,
    alpha=0.9
)

ax.set_title('BMW Price Over Time', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Price', fontsize=12)
ax.tick_params(axis='x', rotation=45)
ax.grid(True, linestyle='--', alpha=0.35)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.show()

# ----------------------------
# 5.2 Average price by year
# ----------------------------
fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(
    avg_price_by_year['year'].astype(str),
    avg_price_by_year['price'],
    color='#2e8b57',
    edgecolor='black',
    linewidth=0.8,
    alpha=0.9
)

ax.set_title('Average BMW Price by Year', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Average Price', fontsize=12)
ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y', linestyle='--', alpha=0.35)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.show()

# ----------------------------
# 5.3 Median price by year
# ----------------------------
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    median_price_by_year['year'],
    median_price_by_year['price'],
    marker='o',
    markersize=7,
    linewidth=2.5,
    color='#c0392b'
)

ax.set_title('Median BMW Price by Year', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Median Price', fontsize=12)
ax.set_xticks(median_price_by_year['year'])
ax.tick_params(axis='x', rotation=45)
ax.grid(True, linestyle='--', alpha=0.35)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.show()

# ----------------------------
# 5.4 Price distribution
# ----------------------------
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(
    df['price'].dropna(),
    bins=20,
    color='#d97b66',
    edgecolor='black',
    alpha=0.85
)

ax.set_title('Distribution of BMW Prices', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Price', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.35)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.show()


# ----------------------------
# 5.5 Outlier analysis
# ----------------------------

prices = df['price'].dropna().values

fig, ax = plt.subplots(figsize=(10, 4))

box = ax.boxplot(
    prices,
    orientation='horizontal',        # ← evita el warning, usa orientación explícita
    patch_artist=True,
    showfliers=True,                 # muestra los puntos outlier
    boxprops=dict(facecolor='#f4c542', color='black', linewidth=1),
    medianprops=dict(color='#8b0000', linewidth=2),
    whiskerprops=dict(color='black', linewidth=1),
    capprops=dict(color='black', linewidth=1),
    flierprops=dict(
        marker='o',
        markerfacecolor='#c0392b',
        markeredgecolor='black',
        markersize=5,
        alpha=0.7
    )
)

ax.set_title('BMW Price – Outlier Analysis (Boxplot)', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Price', fontsize=12)
ax.grid(axis='x', linestyle='--', alpha=0.35)

for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.show()
# ============================
# 6. EXPORT: CLEAN DATASET
# ============================

# Export the clean dataset so it can be used in
# BI tools (Power BI, Tableau, Excel) or other Python scripts.
output_path = 'BMW_CAR_SALES_CLEAN.csv'
df.to_csv(output_path, index=False)

print(f"\nClean file exported to: {output_path}")