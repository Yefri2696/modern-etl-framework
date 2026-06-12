

def extract_from_sql(query, connection_string):
    import pandas as pd
    from sqlalchemy import create_engine

    try:
        engine = create_engine(connection_string)
        df = pd.read_sql(query, engine)
        print("✅ SQL extraction successful.")
        return df.copy()
    except Exception as e:
        raise RuntimeError(f"❌ SQL extraction failed: {e}")

    #conn = directory of SQL server
    #df = extract_from_sql("SELECT * FROM customers", conn)


"""
===========================================================
    EXTRACTORS MODULE — Data Extraction Layer (ETL/ELT)
    Author: Oscar
    Description:
        Conjunto de funciones profesionales para extraer datos
        desde múltiples fuentes: CSV, SQL, NoSQL, APIs, Kafka
        y Web Scraping.
===========================================================
"""

# =========================================================
# 1. CSV / FILES
# =========================================================

def extract_from_csv(path_file = None, encoding=None):

    import pandas as pd
    import os
    import chardet

# 1. Pedir ruta si no se pasa como argumento
    if path_file is None:
        path_file = input("Please enter the file path csv: ").strip()

# 2. Validar existencia del archivo
    if not os.path.exists(path_file):
        raise FileNotFoundError(f"The file path: {path_file} does not exist.")

# 3. Si el usuario especifica encoding manual → usarlo directamente
    if encoding is None:
        try:
            df = pd.read_csv(path_file, encoding=encoding)
            print(f'File loaded successfully used manual encoding: {encoding}')
            return df.copy()

        except Exception as e:
            print(f'Manual encoding: {encoding} failed: {e}')
            print('Switching to automatic detection...')


# 4. Detectar codificación automáticamente
    try:
        with open(path_file, 'rb') as f:
            raw = f.read(50000) # leer 50 KB para detectar
            detected = chardet.detect(raw)
            auto_encoding = detected['encoding']
            confidence = detected['confidence']
        print(f' Encoding detected : {auto_encoding} (confidence : {confidence}')

    except Exception as e:
        print(f'Could not detect encoding automatically: {e}')
        auto_encoding = None

# 5. Intentar leer el CSV con la codificación detectada
    try:
        df = pd.read_csv(path_file, encoding=encoding)
        print (f'File loaded successfully used detected enconding : {encoding}')
        return df.copy()

    except Exception:
        print('Detecting encoding failed. Trying fallback encoding... ')
        fallback = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252', 'windows-1252']

        for enc in fallback:
            try:
                df= pd.read_csv(path_file, encoding=enc)
                print(f'File loaded successfully using fallback encodinf: {enc}')
                return df.copy()
            except Exception:
                continue

        raise RuntimeError('Could not read the CSV with any encoding')


    except pd.errors.EmptyDataError:
        raise ValueError('The file is empty or corrupt.')

    except pd.errors.ParserError:
        raise ValueError('Error parsing the CSV. Check delimiters or encoding.')

    except Exception as e:
        raise RuntimeError(f'Unexpected error: {e}')

    #df = extract_csv(path_file= file directory, encoding=encoding if exist


# =========================================================
# 2. SQL DATABASES
# =========================================================

def extract_from_sql(query, connection_string):
    import pandas as pd
    from sqlalchemy import create_engine

    try:
        engine = create_engine(connection_string)
        df = pd.read_sql(query, engine)
        print("✅ SQL extraction successful.")
        return df.copy()
    except Exception as e:
        raise RuntimeError(f"❌ SQL extraction failed: {e}")


# =========================================================
# 3. NoSQL (MongoDB)
# =========================================================

def extract_from_mongodb(uri, database, collection, query={}):
    import pandas as pd
    from pymongo import MongoClient

    try:
        client = MongoClient(uri)
        col = client[database][collection]
        data = list(col.find(query))
        df = pd.DataFrame(data)
        print("✅ MongoDB extraction successful.")
        return df.copy()
    except Exception as e:
        raise RuntimeError(f"❌ MongoDB extraction failed: {e}")


# =========================================================
# 4. APIs REST
# =========================================================

def extract_from_api(url, headers=None, params=None):
    import requests
    import pandas as pd

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        df = pd.json_normalize(data)
        print("✅ API extraction successful.")
        return df.copy()
    except Exception as e:
        raise RuntimeError(f"❌ API extraction failed: {e}")


# =========================================================
# 5. STREAMING (Kafka)
# =========================================================

def extract_from_kafka(topic, servers, batch_size=100):
    from kafka import KafkaConsumer
    import json
    import pandas as pd

    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=servers,
            auto_offset_reset="earliest",
            consumer_timeout_ms=5000
        )

        messages = []
        for _ in range(batch_size):
            msg = next(consumer)
            messages.append(json.loads(msg.value.decode("utf-8")))

        df = pd.DataFrame(messages)
        print("✅ Kafka extraction successful.")
        return df.copy()

    except Exception as e:
        raise RuntimeError(f"❌ Kafka extraction failed: {e}")


# =========================================================
# 6. WEB SCRAPING
# =========================================================

def extract_from_web(url, parser="html.parser"):
    import requests
    from bs4 import BeautifulSoup

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, parser)
        print("✅ Web scraping extraction successful.")
        return soup
    except Exception as e:
        raise RuntimeError(f"❌ Web scraping failed: {e}")



"""
===========================================================
    EXTRACTION ROUTER — Intelligent Data Source Router
    Author: Oscar
    Description:
        Detecta automáticamente el tipo de fuente de datos
        y llama al extractor correspondiente del módulo
        extractors.py
===========================================================
"""



def extract(source, **kwargs):

    import os
    from urllib.parse import urlparse

    # Importar extractores
    from extract import (
    extract_from_csv,
    extract_from_sql,
    extract_from_mongodb,
    extract_from_api,
    extract_from_kafka,
    extract_from_web)

    """
    Router inteligente que detecta el tipo de fuente y llama
    al extractor adecuado.

    Parámetros:
        source: ruta, URL, cadena SQL, URI MongoDB, topic Kafka
        kwargs: parámetros adicionales para cada extractor

    Retorna:
        DataFrame o BeautifulSoup (según fuente)
    """

    # =========================================================
    # 1. ARCHIVOS (CSV, JSON, PARQUET, etc.)
    # =========================================================
    if os.path.exists(source):
        ext = os.path.splitext(source)[1].lower()

        if ext in [".csv", ".txt", ".zip"]:
            return extract_from_csv(source, **kwargs)

        raise ValueError(f"❌ File type not supported: {ext}")

    # =========================================================
    # 2. URLS (API o WEB)
    # =========================================================
    parsed = urlparse(source)

    if parsed.scheme in ["http", "https"]:
        # API si termina en .json o si headers/params están presentes
        if source.endswith(".json") or "headers" in kwargs or "params" in kwargs:
            return extract_from_api(source, **kwargs)

        # Web scraping
        return extract_from_web(source)

    # =========================================================
    # 3. MONGODB
    # =========================================================
    if source.startswith("mongodb://") or source.startswith("mongodb+srv://"):
        return extract_from_mongodb(source, **kwargs)

    # =========================================================
    # 4. SQL (MySQL, PostgreSQL, SQL Server, etc.)
    # =========================================================
    if any(db in source for db in ["mysql://", "postgresql://", "mssql://", "oracle://", "sqlite:///"]):
        query = kwargs.get("query")
        if not query:
            raise ValueError("❌ SQL extraction requires a 'query' parameter.")
        return extract_from_sql(query, source)

    # =========================================================
    # 5. KAFKA
    # =========================================================
    if source.startswith("kafka://"):
        topic = source.replace("kafka://", "")
        servers = kwargs.get("servers")
        if not servers:
            raise ValueError("❌ Kafka extraction requires 'servers' parameter.")
        return extract_from_kafka(topic, servers, **kwargs)

    # =========================================================
    # 6. FUENTE DESCONOCIDA
    # =========================================================
    raise ValueError("❌ Unknown data source type. Cannot route extraction.")


