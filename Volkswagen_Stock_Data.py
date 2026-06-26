import matplotlib.pyplot as plt
import pandas as pd


from extract import  extract
from transform import TransformPipeline
from transform import ColumnCleaner
from transform import TypeCaster



df1 = extract(r'C:\Users\yefri\OneDrive\Escritorio\datos\Data\Dataset\Volkswagen Stock Data (1995-2026).zip')

pd.set_option('display.max_columns', None)

print(df1.columns)
print(df1.dtypes)
print(df1.head(10))

print(df1.duplicated().sum())
print('********************\n',df1.duplicated('BB_Upper').sum())


pipeline = TransformPipeline([ColumnCleaner(strip=True, lower=True, null_strategy= 0, drop_duplicates=True),
                              TypeCaster({'date': 'auto', 'year': 'datetime', 'month': 'auto', 'low': 'auto'})])

df= pipeline.run(df1)
print(df.dtypes)
print(df.head(10))



'''pipeline = TransformPipeline([
    ColumnCleaner(strip=True, lower=True),
    TypeCaster({"id": int, "cholesterol": int})  # opcional
])'''

df.to_csv('Volkswagen Stock Data (1995-2026).csv', index=False)



