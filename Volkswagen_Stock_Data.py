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

{"code":"# Creating PDF CV for Oscar\nimport matplotlib.pyplot as plt\nfrom matplotlib.backends.backend_pdf import PdfPages\n\ncontent = \"\"\"\nCV – OSCAR ANDRÉS HERNÁNDEZ ULLOA\nCocinero / Capo Partita\n\nForio (NA), Italia\nEmail: yefri962014@hotmail.com\nTel: (+39) 350 062 9476\nNacionalidad: Italiana y Dominicana\nIdiomas: Español (nativo), Italiano (C1), Inglés (A1)\n\nPERFIL PROFESIONAL\nCocinero con experiencia en cocina mediterránea, gestión de partidas, preparación de materia prima y servicios de alta afluencia. Responsable, rápido, organizado y con capacidad para trabajar bajo presión. Busco un puesto como cocinero o capo partita.\n\nEXPERIENCIA LABORAL\nCocinero – Dolce ‘e la Vita (Ischia)\n15/04/2024 – 30/09/2024\n- Preparación de platos, mise en place, control de mercancía, cocciones y emplatado.\n\nCocinero – Ristorante Col’Alt (Corvara, Alta Badia)\n05/12/2024 – 15/04/2025\n- Cocina típica de montaña, gestión de línea, control de stock y emplatado.\n\nCocinero – Ristorante L’Osti (Corvara, Alta Badia)\n01/06/2025 – 15/10/2025\n- Gestión de partida, preparación de carnes, pastas y platos tradicionales.\n\nRosticere – Calise Spresso (Ischia)\n18/05/2023 – 15/09/2023\n- Paninería, frituras, impastos y apoyo en organización del personal.\n\nSegundo Cocinero – Molo 11 (Forio)\n20/06/2021 – 30/09/2021\n- Segundos platos, parrilla, cocciones de pasta y organización de materia prima.\n\nAsistente de Cocina – Ristorante Il Galeone (Forio)\n30/05/2019 – 29/09/2019\n- Frituras, recepción de materia prima, limpieza y emplatado.\n\nEDUCACIÓN\nDiploma de Maturità – Cristofaro Mennella (Ischia)\n2018 – 2024 | EQF 3\n\nCOMPETENCIAS\n- Gestión de partidas\n- Cocciones de pasta, carne y pescado\n- Preparación de materia prima\n- Emplatado y control de calidad\n- Trabajo bajo presión\n- Higiene y seguridad alimentaria\n\nPERMISOS DE CONDUCIR\nA – B\n\"\"\"\n\npdf_path = \"/mnt/data/CV_Oscar_Hernandez.pdf\"\nwith PdfPages(pdf_path) as pdf:\n    fig = plt.figure(figsize=(8.27, 11.69))\n    plt.text(0.01, 0.99, content, va='top', fontsize=10, family='monospace')\n    plt.axis('off')\n    pdf.savefig(fig)\n    plt.close()\n\nprint(f\"PDF generado correctamente: {pdf_path}\")"}
