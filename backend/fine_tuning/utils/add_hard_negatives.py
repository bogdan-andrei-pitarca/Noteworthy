import pandas as pd
import os
import random
import ast 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAIRS_PATH = os.path.join(BASE_DIR, 'datasets', 'sbert', 'sbert_query_pairs.csv')
DB_PATH = os.path.join(os.path.dirname(BASE_DIR), 'data', 'fra_data_processed.csv')
OUTPUT_PATH = os.path.join(BASE_DIR, 'datasets', 'sbert', 'sbert_triplets.csv')

print("Loading data...")
pairs_df = pd.read_csv(PAIRS_PATH)
db_df = pd.read_csv(DB_PATH)

db_map = db_df.set_index('embedding_id').to_dict('index')

triplets = []
skipped = 0

for _, row in pairs_df.iterrows():
    emb_id = row['embedding_id']
    if pd.isna(emb_id):
        print("Warning: Missing embedding_id in pairs dataset. Skipping row.")
        skipped += 1
        continue
    target_perfume = db_map.get(emb_id)

    if not target_perfume:
        print(f"Warning: embedding_id {emb_id} not found in database. Skipping.")
        skipped += 1
        continue

    target_accord = target_perfume.get('mainaccord1')
    target_gender = target_perfume.get('Gender')

    # hard negative rule: same accord, same gender, different ID
    candidates = db_df[
        (db_df['mainaccord1'] == target_accord) &
        (db_df['Gender'] == target_gender) &
        (db_df['embedding_id'] != emb_id)
    ]

    if candidates.empty:
        print(f"No hard negative found for embedding_id {emb_id} with accord {target_accord} and gender {target_gender}")
        skipped += 1
        continue

    else:
        negative_row = candidates.sample(1).iloc[0]

        triplets.append({
            'embedding_id': emb_id,
            'anchor': row['anchor'],
            'positive': row['positive'],
            'negative': negative_row['embedding_text'],
            'negative_embedding_id': negative_row['embedding_id']
        })

triplets_df = pd.DataFrame(triplets)
triplets_df.to_csv(OUTPUT_PATH, index=False)
print(f"Saved {len(triplets)} triplets to {OUTPUT_PATH}")
print(f"\nSample triplet:")
print(f"Anchor: {triplets_df.iloc[0]['anchor']}")
print(f"Positive: {triplets_df.iloc[0]['positive'][:100]}")
print(f"Negative: {triplets_df.iloc[0]['negative'][:100]}")
print(f"Skipped: {skipped} rows")