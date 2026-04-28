import pandas as pd
import ast
import os

# paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLDEN_DATASET_PATH = os.path.join(BASE_DIR, 'datasets', 'claude', 't5_golden_dataset_claude_v2.csv')
SBERT_DATA_PATH = os.path.join(BASE_DIR, 'datasets', 'sbert', 'sbert_training_data.csv')

def prepare_data():
    if not os.path.exists(GOLDEN_DATASET_PATH):
        print(f"Error: Golden dataset not found at {GOLDEN_DATASET_PATH}")
        return
    
    df = pd.read_csv(GOLDEN_DATASET_PATH)

    # we need description and notes
    pairs = []
    for _, row in df.iterrows():
        anchor = row['target_description']

        # clean notes from ['note1', 'note2'] format to "note1, note2"
        try:
            notes_list = ast.literal_eval(row['all_notes'])
            positive = ', '.join(notes_list)
        except:
            positive = row['all_notes']  # fallback to raw string if parsing fails
        
        pairs.append({'anchor': anchor, 'positive': positive})

    pd.DataFrame(pairs).to_csv(SBERT_DATA_PATH, index=False)
    print(f"Prepared SBERT training data saved to {SBERT_DATA_PATH}")

if __name__ == "__main__":
    prepare_data()