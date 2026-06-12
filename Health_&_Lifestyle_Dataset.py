import pandas as pd
import matplotlib.pyplot as plt


file_path = r'C:\Users\yefri\OneDrive\Escritorio\datos\Visualizacion de datos\Dataset\Health & Lifestyle Dataset.zip'

df = pd.read_csv(file_path, encoding="windows-1252")

print(df.duplicated().sum())
print(df.isnull().sum())

def delete_duplicates_null (df):
    df.drop_duplicates(subset=None, keep='last', inplace=True)
    df. dropna(how='all', subset=['id'], axis=0, inplace=True)
    return df


delete_duplicates_null(df)
print(df.duplicated().sum())
print(df.isnull().sum())



def delete_duplicates_nulls (df, key_cols=['col']):
    df = df.copy()

    #Validate columns
    missing = [col for col in key_cols if col not in df.columns]
    if missing:
        raise ValueError(f'The following columns are missing: {missing}')

    #Delete Duplicates
    before = len(df)
    df.drop_duplicates(subset=key_cols, keep='last', inplace=True)

    print(f'After {before - len(df)} duplicates removed')

    #Delete null Value
    before = len(df)
    df.dropna(how='any', subset= key_cols, inplace=True)

    print(f'After {before - len(df)} null values removed')

    return df
df_cleaned = delete_duplicates_nulls(df, key_cols=['id'])



res = []
for i in range(3):
    for j in range(3):
        if j == 1:
            break
        res.append(i)

print(res)