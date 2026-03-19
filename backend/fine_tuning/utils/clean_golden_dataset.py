import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_PATH = os.path.join(BASE_DIR, 'datasets', 't5_golden_dataset.csv')
OUTPUT_PATH = os.path.join(BASE_DIR, 'datasets', 't5_golden_dataset_cleaned.csv')

if not os.path.exists(INPUT_PATH):
    print(f"Error: Input file not found at {INPUT_PATH}. Please run the previous steps first.")
else:
    df = pd.read_csv(INPUT_PATH)

    # list of repetitive phrases to target
    cliches = [
        "As the fragrance unfolds",
        "As the scent unfurls",
        "This fragrance is like",
        "stepping into a sun-kissed"
    ]

    # keep rows that DO NOT start with these phrases
    pattern = '|'.join([f"^{phrase}" for phrase in cliches])
    original_count = len(df)

    # filter
    df_cleaned = df[~df['target_description'].str.contains(pattern, case=False, na=False)]

    print(f"Original rows: {original_count}")
    print(f"Rows kept: {len(df_cleaned)}")
    print(f"Rows deleted: {original_count - len(df_cleaned)}")

    # save the clean version (the keepers)
    df_cleaned.to_csv(OUTPUT_PATH, index=False)
    print(f"Cleaned dataset saved to {OUTPUT_PATH}")