from pandas.core.arrays import datetimes


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
    def __init__(
        self,
        strip=True,
        lower=True,
        drop_duplicates=False,
        null_strategy=None,      # 'mean', 'median', 'mode', 'drop', valor fijo
        null_columns=None        # columnas a aplicar la estrategia
    ):
        self.strip = strip
        self.lower = lower
        self.drop_duplicates = drop_duplicates
        self.null_strategy = null_strategy
        self.null_columns = null_columns

    def transform(self, df):
        import pandas as pd
        import logging

        logging.info("Iniciando limpieza de columnas")

        # ---------------------------------------------------------
        # 1) LIMPIEZA DE NOMBRES DE COLUMNAS
        # ---------------------------------------------------------
        new_cols = []
        for col in df.columns:
            new_col = col
            if self.strip:
                new_col = new_col.strip()
            if self.lower:
                new_col = new_col.lower()
            new_cols.append(new_col)

        df.columns = new_cols

        # ---------------------------------------------------------
        # 2) LIMPIEZA DE VALORES DE TEXTO
        # ---------------------------------------------------------
        for col in df.select_dtypes(include="object").columns:
            if self.strip:
                df[col] = df[col].str.strip()
            if self.lower:
                df[col] = df[col].str.lower()

        # ---------------------------------------------------------
        # 3) ELIMINACIÓN OPCIONAL DE DUPLICADOS
        # ---------------------------------------------------------
        if self.drop_duplicates:
            before = len(df)
            df = df.drop_duplicates()
            logging.info(f"Duplicados eliminados: {before - len(df)}")

        # ---------------------------------------------------------
        # 4) TRATAMIENTO DE NULOS (media, mediana, moda, drop, valor fijo)
        # ---------------------------------------------------------
        if self.null_strategy is not None:

            # Si no se especifican columnas, aplicar a todas
            cols = self.null_columns or df.columns

            for col in cols:
                if col not in df.columns:
                    logging.warning(f"Columna '{col}' no existe en el DataFrame")
                    continue

                if self.null_strategy == "drop":
                    before = len(df)
                    df = df.dropna(subset=[col])
                    logging.info(f"Filas eliminadas por nulos en '{col}': {before - len(df)}")
                    continue

                if df[col].isna().sum() == 0:
                    continue  # nada que imputar

                if self.null_strategy == "mean":
                    value = df[col].mean()

                elif self.null_strategy == "median":
                    value = df[col].median()

                elif self.null_strategy == "mode":
                    value = df[col].mode().iloc[0]

                else:
                    # valor fijo proporcionado por el usuario
                    value = self.null_strategy

                df[col] = df[col].fillna(value)
                logging.info(f"Nulos en '{col}' reemplazados por: {value}")

        logging.info("Limpieza completada")
        return df




# transform/type_casting.py
class TypeCaster:
    def __init__(self, type_map: dict):
        """
        type_map:
            - "auto" → detectar automáticamente
            - "int", "float", "string", "datetime", "year", "month", "day" → manual
        """
        self.type_map = type_map

    # ---------------------------------------------------------
    # DETECCIÓN AUTOMÁTICA
    # ---------------------------------------------------------
    def _detect_auto_type(self, series):
        import pandas as pd

        s = series.dropna().astype(str)

        # ---------- INT ----------
        if s.str.fullmatch(r"[+-]?\d+").all():
            vals = s.astype(int)

            if vals.between(1000, 2100).all():
                return "year"

            if vals.between(1, 12).all():
                return "month"

            if vals.between(1, 31).all():
                return "day"

            return "int"

        # ---------- FLOAT ----------
        if s.str.fullmatch(r"[+-]?\d+(\.\d+)?").all():
            return "float"

        # ---------- FECHAS ----------
        if s.str.fullmatch(r"\d{4}-\d{2}-\d{2}").all():
            return {"type": "datetime", "format": "%Y-%m-%d"}

        if s.str.fullmatch(r"\d{1,2}[/-]\d{1,2}[/-]\d{4}").all():
            return {"type": "datetime", "format": "dayfirst"}

        if s.str.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}").all():
            return {"type": "datetime", "format": "monthfirst"}

        # ---------- TIMESTAMP COMPACTO ----------
        compact_formats = {
            r"\d{14}": "%Y%m%d%H%M%S",
            r"\d{12}": "%Y%m%d%H%M",
            r"\d{10}": "%Y%m%d%H",
            r"\d{8}": ["%Y%m%d", "%d%m%Y"],
            r"\d{6}": "%y%m%d",
        }

        for pattern, fmt in compact_formats.items():
            if s.str.fullmatch(pattern).all():
                return {"type": "datetime", "format": fmt if not isinstance(fmt, list) else fmt[0]}

        # ---------- PARSEO AUTOMÁTICO ----------
        try:
            parsed = pd.to_datetime(s, errors="coerce", dayfirst=True)
            if parsed.notna().mean() > 0.8:
                return "datetime_auto"
        except:
            pass

        return "string"

    # ---------------------------------------------------------
    # TRANSFORMACIÓN
    # ---------------------------------------------------------
    def transform(self, df):
        import pandas as pd

        detected = {}

        # 1. Detectar tipos (manual o automático)
        for col, dtype in self.type_map.items():
            if dtype == "auto":
                detected[col] = self._detect_auto_type(df[col])
            else:
                detected[col] = dtype

        # 2. Aplicar conversiones
        for col, dtype in detected.items():

            # ---------- INT ----------
            if dtype == "int":
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

            # ---------- FLOAT ----------
            elif dtype == "float":
                df[col] = pd.to_numeric(df[col], errors="coerce")

            # ---------- STRING ----------
            elif dtype == "string":
                df[col] = df[col].astype(str)

            # ---------- YEAR / MONTH / DAY ----------
            # NO convertir a fecha, solo reconocerlos
            elif dtype in ("year", "month", "day"):
                df[col] = df[col].astype(int)

            # ---------- DATETIME AUTO ----------
            elif dtype == "datetime_auto":
                df[col] = pd.to_datetime(df[col], errors="coerce")

            # ---------- DATETIME CON FORMATO ----------
            elif isinstance(dtype, dict) and dtype.get("type") == "datetime":
                fmt = dtype["format"]

                if fmt == "dayfirst":
                    df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
                elif fmt == "monthfirst":
                    df[col] = pd.to_datetime(df[col], errors="coerce")
                else:
                    df[col] = pd.to_datetime(df[col], format=fmt, errors="coerce")

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
'''if __name__ == "__main__":
    import pandas as pd

    # Simulación de datos extraídos (como si vinieran de EXTRACT)
    df = pd.DataFrame({
        "id": [" 1 ", " 2 "],
        "name": [" Oscar ", " Ana "],
        "created_at": ["2024-01-01", "2024-01-02"]
    })

    df_final = run_transform(df)

    print("\n=== DataFrame Transformado ===")
    print(df_final)'''
