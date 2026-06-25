from pandas.core.tools import datetimes

from extract import extract
from transform import TransformPipeline
from transform import ColumnCleaner
from transform import TypeCaster

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd

df = extract(r'C:\Users\yefri\OneDrive\Escritorio\datos\Data\Dataset\BMW Car sales and Price Dataset.zip')

print(df.head(10))

print(df.duplicated().sum)
print(df.isnull().sum())
print(df.dtypes)

pipeline = TransformPipeline([ColumnCleaner(strip=True, lower=True),
                              TypeCaster({'year':'datetime'})])
df = pipeline.run(df)
print(df.head(10))

plt.figure(figsize=(10,5))
plt.scatter(df['year'], df['price'], label='Price', color='red', marker='o')
plt.xticks(rotation=45)
plt.legend()
plt.title('Price by Year')
plt.xlabel('Year')
plt.ylabel('Price')
plt.show()

df['year'] = pd.to_datetime(df['year'], format='%Y')
year = df.groupby(df['year'])['price'].sum()

plt.plot(year.index, year.values)
plt.gca().xaxis.set_major_formatter(DateFormatter('%Y'))
plt.xticks(rotation=45)

plt.title('Time series by Year')
plt.xlabel('Years')
plt.ylabel('Value')
plt.tight_layout()
plt.show()



plt.figure(figsize = (8,6))
plt.plot(df['year'],df['price'], marker='o', color = 'blue', linewidth = 2, linestyle = '-', label = 'price')
plt.title('exam_score vs student score by two students')
plt.xlabel('year')
plt.ylabel('price')
plt.legend(loc='upper left')
plt.show()


df.to_csv('BMW_CAR_SALES.csv', index = False)