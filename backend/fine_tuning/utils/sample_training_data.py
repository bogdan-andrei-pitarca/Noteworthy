import sys
import pandas as pd
import os

# paths
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(UTILS_DIR) # fine_tuning
BACKEND_DIR = os.path.dirname(BASE_DIR) # backend
SOURCE_PATH = os.path.join(BACKEND_DIR, 'data', 'fra_data_processed.csv')
OUTPUT_PATH = os.path.join(BASE_DIR, 'datasets', 't5_sample_stratified.csv')

sys.path.append(os.path.join(BASE_DIR, 'utils'))
from sampling import get_stratified_sample

TARGET_TOTAL = 1000
RATING_COL = 'Rating Count'
ACCORD_COL = 'mainaccord1'
NOTES_COL = 'all_notes'


def main():
    print(f"Loading source data from {SOURCE_PATH}...")

    if not os.path.exists(SOURCE_PATH):
        raise FileNotFoundError(f"Source file not found at {SOURCE_PATH}. Please run the previous steps first.")
    
    df_raw = pd.read_csv(SOURCE_PATH, encoding='latin1')
    print(f"Source data loaded: {len(df_raw)} rows.")

    sample_df = get_stratified_sample(df_raw, TARGET_TOTAL)

    # save only needed columns

    cols_to_save = ['embedding_id', ACCORD_COL, NOTES_COL]
    output_df = sample_df[cols_to_save]

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    output_df.to_csv(OUTPUT_PATH, index=False)

    # summary

    print(f"\n{'-'*40}\nSample saved to {OUTPUT_PATH}")
    print(f"\nFamily distribution in sample:")
    dist = output_df[ACCORD_COL].value_counts()
    for family, count in dist.items():
        print(f"Family '{family:<30}': {count} perfumes")
    print(f"{'-'*40}")

if __name__ == "__main__":
    main()