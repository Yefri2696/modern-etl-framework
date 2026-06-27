"""Pipeline: Volkswagen Stock Data (1995–2026)
Author: Oscar Hernández
Goal:
- Extract historical Volkswagen stock data
- Clean, normalize, and convert data types
- Prepare dataset for financial analysis and dashboards

Flow:
Extract → Clean → TypeCast → Export"""

import pandas as pd
<<<<<<< HEAD
import matplotlib.pyplot as plt
=======
>>>>>>> 5552d2d840f915a0d5d271bbfe6591410eba10db
from extract import  extract
from transform import TransformPipeline
from transform import ColumnCleaner
from transform import TypeCaster


#==========================================
#1. EXTRACT
#==========================================

df1 = extract(r'C:\Users\yefri\OneDrive\Escritorio\datos\Data\Dataset\Volkswagen Stock Data (1995-2026).zip')

pd.set_option('display.max_columns', None)

print(df1.columns)
print(df1.dtypes)
print(df1.head(10))

#=========================================
#2. QUALITY CHECKS
#=========================================

print(df1.duplicated().sum())
print('********************\n',df1.duplicated('BB_Upper').sum())

#==========================================
#3. TRANSFORM PIPELINE
#==========================================
pipeline = TransformPipeline([ColumnCleaner(strip=True, lower=True, null_strategy= 0, drop_duplicates=True),
                              TypeCaster({'date': 'auto', 'year': 'datetime', 'month': 'auto', 'low': 'auto'})])

df= pipeline.run(df1)
print(df.dtypes)
print(df.head(10))

#========================================
#4. EXPORT
#=======================================
df.to_csv('Volkswagen Stock Data (1995-2026) clean.csv', index=False)
<<<<<<< HEAD

# ============================
# 5. KPIs
# ============================

kpis = {
    "Min Price": df['low'].min(),
    "Max Price": df['high'].max(),
    "Average Price": df['close'].mean(),
    "Total Volume": df['volume'].sum(),
    "Average Volume": df['volume'].mean(),
    "Total Performance (%)": ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
}

print("\n===== KPIs =====")
for k, v in kpis.items():
    print(f"{k}: {v}")


# ============================
# 6. TRENDS
# ============================

df['year'] = df['date'].dt.year

trend_close = df.groupby('year')['close'].mean()
trend_volume = df.groupby('year')['volume'].sum()

print("\n===== AVERAGE PRICE TREND PER YEAR =====")
print(trend_close)

print("\n===== TOTAL VOLUME TREND BY YEAR =====")
print(trend_volume)



# ============================
# 7. GRAPHICS
# ============================

plt.figure(figsize=(12,5))
plt.plot(df['date'], df['close'], label='Close Price', color='blue')
plt.title("Volkswagen Stock Price (1995–2026)")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.grid(True)
plt.legend()
plt.show()

plt.figure(figsize=(12,5))
plt.plot(trend_close.index, trend_close.values, marker='o', color='green')
plt.title("Average Trend by Year")
plt.xlabel("Year")
plt.ylabel("Average Price")
plt.grid(True)
plt.show()

plt.figure(figsize=(12,5))
plt.bar(trend_volume.index, trend_volume.values, color='orange')
plt.title("Total Volume by Year")
plt.xlabel("Year")
plt.ylabel("Total Volume")
plt.show()


# ============================
# 8. TEMPORAL RANGE
# ============================

start_date = df['date'].min()
end_date = df['date'].max()

print("\n===== TEMPORAL RANGE =====")
print(f"From: {start_date}")
print(f"To: {end_date}")


# ============================
# 9. DESCRIPTIVE STATISTICS
# ============================

print("\n===== Descriptive Statistics =====")
print(df.describe())

=======



>>>>>>> 5552d2d840f915a0d5d271bbfe6591410eba10db
