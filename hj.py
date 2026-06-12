
from extract import  extract
from transform import run_transform

from transform import TransformPipeline
from transform import ColumnCleaner
from transform import TypeCaster
from transform import SchemaValidator








df1 = extract(r'C:\Users\yefri\OneDrive\Escritorio\datos\Data\Dataset\Health & Lifestyle Dataset.zip')

print(df1.columns)

print(df1.duplicated().sum())

pipeline = TransformPipeline([
    ColumnCleaner(strip=True, lower=True),
    TypeCaster({"id": int, "cholesterol": int})  # opcional
])

df_transformed = pipeline.run(df1)
print(df_transformed.head(10))



