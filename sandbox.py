import pandas as pd
import numpy as np

# creating a dffrom a dix

data = {
    'language': ['English', 'French', 'Xhosa', 'Kree'],
    'segments': [1200, 640, 230, 100],
    'translated': [1200, 600, 210, 90],
    'review_done': [True, False, True, False]
}

df = pd.DataFrame(data)
print(df)
print(df.shape)
print(df.dtypes)

print(df['language'])
print(df.iloc[1])
print(df.loc[2, 'segments'])

incomplete = df[df['translated'] < df['segments']]
print(incomplete)

#df['coverage'] = df['translated'] / df['segments']
print(df)

not_reviewed = df[df['review_done'] == False]
print(not_reviewed)

df.loc[1, 'translation'] = np.nan
df.loc[3, 'coverage'] = np.nan

print(df)
print(df.isnull().sum)
print(df.dropna())
print(df.fillna(0))

