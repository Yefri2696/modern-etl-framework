
'''✅ 1. schema_validator.py (opcional, universal)
Si el usuario define un esquema, se valida.
Si no, simplemente no se usa.'''

class SchemaValidator:
    def __init__(self, schema):
        self.schema = schema

    def transform(self, df):
        import logging
        from pydantic import ValidationError

        errors = []

        for idx, row in df.iterrows():
            try:
                self.schema(**row.to_dict())
            except ValidationError as e:
                errors.append((idx, e.errors()))

        if errors:
            logging.error(f"Errores de validación: {errors[:5]}")
            raise ValueError("El DataFrame no cumple el esquema definido")

        logging.info("Validación de esquema completada")
        return df


'''✅ 2. cleaning.py (funciona con cualquier dataset)
Este limpiador:

Detecta columnas string automáticamente

Limpia sin romper datos numéricos

No depende de nombres de columnas'''

class ColumnCleaner:
    def __init__(self, strip=True, lower=False):
        self.strip = strip
        self.lower = lower

    def transform(self, df):
        import logging

        logging.info("Iniciando limpieza universal de columnas")

        object_cols = df.select_dtypes(include="object").columns

        for col in object_cols:
            if self.strip:
                df[col] = df[col].astype(str).str.strip()
            if self.lower:
                df[col] = df[col].astype(str).str.lower()

        logging.info("Limpieza completada")
        return df



'''✅ 3. type_casting.py (dinámico y universal)
Permite:

Convertir tipos si el usuario lo desea

Ignorar columnas no especificadas

No depende de la fuente'''

class TypeCaster:
    def __init__(self, type_map: dict = None):
        self.type_map = type_map or {}

    def transform(self, df):
        import logging

        logging.info("Normalización de tipos iniciada")

        for col, dtype in self.type_map.items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)

        logging.info("Normalización de tipos completada")
        return df


'''✅ 4. pipeline.py (universal)
Funciona con cualquier DataFrame, de cualquier extractor.'''

class TransformPipeline:
    def __init__(self, steps):
        self.steps = steps

    def run(self, df):
        for step in self.steps:
            df = step.transform(df)
        return df



'''Cómo usarlo en tu ETL
python
from transform.pipeline import TransformPipeline
from transform.cleaning import ColumnCleaner
from transform.type_casting import TypeCaster
from transform.schema_validator import SchemaValidator
from schemas.sales_schema import SalesSchema  # tu esquema Pydantic

pipeline = TransformPipeline([
    SchemaValidator(SalesSchema()),
    ColumnCleaner(strip=True, lower=True),
    TypeCaster({"price": float, "quantity": int})
])

df_final = pipeline.run(df_raw)'''

