import pandas as pd
import os

# paths
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(UTILS_DIR) # fine_tuning
BACKEND_DIR = os.path.dirname(BASE_DIR) # backend
SOURCE_PATH = os.path.join(BACKEND_DIR, 'data', 'fra_data_processed.csv')
OUTPUT_PATH = os.path.join(BASE_DIR, 'datasets', 't5_sample_stratified.csv')

TARGET_TOTAL = 1000
RATING_COL = 'Rating Count'
ACCORD_COL = 'mainaccord1'
NOTES_COL = 'all_notes'

def stratified_sample(df: pd.DataFrame, target: int) -> pd.DataFrame:
    """
    Samples target amount of rows from df, DISTRIBUTED EVENLY across scent families (mainaccord1).
    Within each family, samples the most popular perfumes (by rating count) to ensure quality data.
    Strategy:
    1. Calculate a per-family budget = target / number of unique families
    2. For each family, sort by rating count and take up to the per-family budget (if there are fewer perfumes than the budget, take them all)
    3. If certain families are smaller than the budget and we are under target => top up from the remaining pool until we hit 'target'.
    """
    for col in [ACCORD_COL, RATING_COL, NOTES_COL]:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame.")
        
    # drop rows with missing accord or notes (can't stratify without them)
    df = df.dropna(subset=[ACCORD_COL, NOTES_COL]).copy()
    df[RATING_COL] = pd.to_numeric(df[RATING_COL], errors='coerce').fillna(0) # ensure rating count is numeric, fill non-convertible with 0

    # drop families too small -> avoids noise
    MIN_FAMILY_SIZE = 3
    family_sizes = df.groupby(ACCORD_COL)[ACCORD_COL].transform('count')
    dropped_families = df[family_sizes < MIN_FAMILY_SIZE][ACCORD_COL].unique()
    if len(dropped_families) > 0:
        print(f"Dropping {len(dropped_families)} families with fewer than {MIN_FAMILY_SIZE} perfumes: {', '.join(dropped_families)}")
    df = df[family_sizes >= MIN_FAMILY_SIZE]

    # drop rows where all notes are the same token (garbage)
    def is_garbage(notes):
        try:
            notes = eval(notes)
            unique = set(n.strip().lower() for n in notes)
            return len(unique) <= 1
        except:
            return False 

    before = len(df)
    df = df[~df[NOTES_COL].apply(is_garbage)]
    removed = before - len(df)
    if removed > 0:
        print(f"Dropped {removed} rows with non-informative notes.")

    groups = df.groupby(ACCORD_COL)
    n_families = groups.ngroups
    per_family_budget = target // n_families

    print(f"\n Found {n_families} scent families in {ACCORD_COL}.")
    print(f" Target sample size: {target}")
    print(f" Per-family budget: {per_family_budget}")

    # step 1
    sampled_parts = []
    for family, group in groups:
        take = group.nlargest(min(per_family_budget, len(group)), RATING_COL)
        sampled_parts.append(take)
        print(f"Family '{family:<30}': {len(group):<5} perfumes, taking {len(take)}")

    sample_df = pd.concat(sampled_parts).reset_index(drop=True)

    # step 2 - top up if under target
    shortfall = target - len(sample_df)
    if shortfall > 0:
        sampled_ids = set(sample_df.index)
        # since we reset index, we compare on embedding id
        sampled_eids = set(sample_df['embedding_id'])
        remaining = df[~df['embedding_id'].isin(sampled_eids)]
        top_up = remaining.nlargest(shortfall, RATING_COL)
        sample_df = pd.concat([sample_df, top_up]).reset_index(drop=True)
        print(f"\n Sampled {len(sample_df)} perfumes after top-up (added {len(top_up)} from remaining pool).")

    # shuffle the final sample to mix families up
    sample_df = sample_df.sample(frac=1, random_state=42).reset_index(drop=True)

    return sample_df

def main():
    print(f"Loading source data from {SOURCE_PATH}...")

    if not os.path.exists(SOURCE_PATH):
        raise FileNotFoundError(f"Source file not found at {SOURCE_PATH}. Please run the previous steps first.")
    
    df_raw = pd.read_csv(SOURCE_PATH, encoding='latin1')
    print(f"Source data loaded: {len(df_raw)} rows.")

    sample_df = stratified_sample(df_raw, TARGET_TOTAL)

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