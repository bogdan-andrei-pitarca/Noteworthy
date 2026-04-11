import pandas as pd
import os

# paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')
CLAUDE_DIR = os.path.join(DATASETS_DIR, 'claude')

input_path = os.path.join(CLAUDE_DIR, 't5_golden_dataset_claude.csv')
df = pd.read_csv(input_path)

def is_scene_based(text):
    text_lower = text.lower()
    patterns = [
        'walking past', 'walking through', 'walking into',
        'where someone', 'someone just', 'stepping into'
    ]
    return any(p in text_lower for p in patterns)

mask = df['target_description'].apply(is_scene_based)
print(f"Scene-based rows to regenerate: {mask.sum()}")

df_keep = df[~mask]
df_regenerate = df[mask]

df_keep.to_csv(os.path.join(DATASETS_DIR, 't5_golden_keep.csv'), index=False)
df_regenerate[['all_notes', 'mainaccord1', 'embedding_id']].to_csv(os.path.join(DATASETS_DIR, 't5_golden_regenerate.csv'), index=False)