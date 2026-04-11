import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FINE_TUNING_DIR = os.path.dirname(SCRIPT_DIR) 

DATASETS_DIR = os.path.join(FINE_TUNING_DIR, 'datasets')
CLAUDE_DIR = os.path.join(DATASETS_DIR, 'claude')

df_keep = pd.read_csv(os.path.join(DATASETS_DIR, 't5_golden_keep.csv'))
df_regen = pd.read_csv(os.path.join(CLAUDE_DIR, 't5_golden_dataset_claude.csv'))

print(f"Keep rows: {len(df_keep)}")
print(f"Regenerated rows: {len(df_regen)}")

df_final = pd.concat([df_keep, df_regen], ignore_index=True)

# sanity checks
print(f"Total rows: {len(df_final)}")
print(f"Duplicate embedding_ids: {df_final['embedding_id'].duplicated().sum()}")
print(f"Missing descriptions: {df_final['target_description'].isna().sum()}")

# shuffle so keep and regen rows are mixed
df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)

df_final.to_csv(f'{CLAUDE_DIR}/t5_golden_dataset_claude_v2.csv', index=False)
print("Saved to t5_golden_dataset_claude_v2.csv")