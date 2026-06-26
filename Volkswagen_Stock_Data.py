"""Pipeline: Volkswagen Stock Data (1995–2026)
Author: Oscar Hernández
Goal:
- Extract historical Volkswagen stock data
- Clean, normalize, and convert data types
- Prepare dataset for financial analysis and dashboards

Flow:
Extract → Clean → TypeCast → Export"""

import pandas as pd
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



