


# transform/base_transformer.py
class BaseTransformer:
    def log(self, message: str):
        import logging
        logging.info(f"[TRANSFORM] {message}")

    def transform(self, df):
        raise NotImplementedError("Debes implementar el método transform()")



# transform/schema_validator.py
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



# transform/cleaning.py
class ColumnCleaner:
    def __init__(self, strip=True, lower=True):
        self.strip = strip
        self.lower = lower

    def transform(self, df):
        import pandas as pd
        import logging

        logging.info("Iniciando limpieza de columnas")

        for col in df.select_dtypes(include="object").columns:
            if self.strip:
                df[col] = df[col].str.strip()
            if self.lower:
                df[col] = df[col].str.lower()

        logging.info("Limpieza completada")
        return df


# transform/type_casting.py
class TypeCaster:
    def __init__(self, type_map: dict):
        self.type_map = type_map

    def transform(self, df):
        import logging

        logging.info("Normalización de tipos iniciada")

        for col, dtype in self.type_map.items():
            df[col] = df[col].astype(dtype)

        logging.info("Normalización de tipos completada")
        return df


# transform/enrichment.py
class SalesEnricher:
    def transform(self, df):
        import logging

        logging.info("Enriquecimiento de datos iniciado")

        df["total"] = df["price"] * df["quantity"]
        df["is_high_value"] = df["total"] > 100

        logging.info("Enriquecimiento completado")
        return df


# transform/pipeline.py
class TransformPipeline:
    def __init__(self, steps):
        self.steps = steps

    def run(self, df):
        for step in self.steps:
            df = step.transform(df)
        return df


# run_transform.py

def run_transform(df):
    """
    Ejecuta un pipeline universal de transformación sobre cualquier DataFrame.
    Todas las importaciones están dentro de las funciones para evitar dependencias globales.
    """

    # ============================
    # IMPORTACIONES INTERNAS
    # ============================
    from transform import (TransformPipeline,ColumnCleaner, TypeCaster,SchemaValidator,MySchema)  # opcional


    # ============================
    # CONSTRUCCIÓN DEL PIPELINE
    # ============================
    pipeline = TransformPipeline([
        SchemaValidator(MySchema),                 # Validación opcional
        ColumnCleaner(strip=True, lower=True),     # Limpieza universal
        TypeCaster({                               # Normalización opcional
            "id": int,
            "created_at": "datetime64[ns]"
        })
    ])

    # ============================
    # EJECUCIÓN DEL PIPELINE
    # ============================
    df_transformed = pipeline.run(df)

    return df_transformed



# ============================
# EJEMPLO DE USO DIRECTO
# ============================
if __name__ == "__main__":
    import pandas as pd

    # Simulación de datos extraídos (como si vinieran de EXTRACT)
    df = pd.DataFrame({
        "id": [" 1 ", " 2 "],
        "name": [" Oscar ", " Ana "],
        "created_at": ["2024-01-01", "2024-01-02"]
    })

    df_final = run_transform(df)

    print("\n=== DataFrame Transformado ===")
    print(df_final)
