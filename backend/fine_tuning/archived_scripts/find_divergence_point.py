import pandas as pd
df1 = pd.read_csv('data/fra_data_with_descriptions.csv')
df2 = pd.read_csv('data/fra_data_processed.csv')
print(f'with_descriptions rows: {len(df1)}')
print(f'processed rows: {len(df2)}')
print(f'MATCH: {len(df1) == len(df2)}')
r1 = df1[df1['embedding_id'] == 7670][['Perfume','Brand']].values
r2 = df2[df2['embedding_id'] == 7670][['Perfume','Brand']].values
print(f'ID 7670 matches: {r1} == {r2} -> {r1[0][0] == r2[0][0]}')