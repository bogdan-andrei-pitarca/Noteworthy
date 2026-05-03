# File: backend/fine_tuning/utils/sampling.py
import pandas as pd
import ast

def get_stratified_sample(df: pd.DataFrame, target: int) -> pd.DataFrame:
    """
    Samples target amount of rows from df, DISTRIBUTED EVENLY across scent families (mainaccord1).
    Within each family, samples the most popular perfumes (by rating count) to ensure quality data.
    Strategy:
    1. Calculate a per-family budget = target / number of unique families
    2. For each family, sort by rating count and take up to the per-family budget (if there are fewer perfumes than the budget, take them all)
    3. If certain families are smaller than the budget and we are under target => top up from the remaining pool until we hit 'target'.
    """
    for col in ['mainaccord1', 'Rating Count', 'all_notes']:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame.")
    # 1. Drop rows with missing crucial data
    df = df.dropna(subset=['mainaccord1', 'all_notes']).copy()
    
    # 2. Ensure numeric rating count
    df['Rating Count'] = pd.to_numeric(df['Rating Count'], errors='coerce').fillna(0)

    # 3. Drop families that are too small (noise reduction)
    MIN_FAMILY_SIZE = 3
    family_sizes = df.groupby('mainaccord1')['mainaccord1'].transform('count')
    df = df[family_sizes >= MIN_FAMILY_SIZE]

    # 4. Drop garbage rows where notes are uninformative/repetitive
    def is_garbage(notes_str):
        try:
            # Safely evaluate the string list (no unsafe eval!)
            notes_list = ast.literal_eval(notes_str)
            unique = set(n.strip().lower() for n in notes_list)
            return len(unique) <= 1
        except:
            return True # If it can't be parsed, it's garbage

    print(f"Dropping {df['all_notes'].apply(is_garbage).sum()} rows with non-informative notes.")
    df = df[~df['all_notes'].apply(is_garbage)]

    # 5. Calculate Budget
    groups = df.groupby('mainaccord1')
    n_families = groups.ngroups
    per_family_budget = target // n_families

    # 6. Sample evenly
    sampled_parts = []
    for family, group in groups:
        take = group.nlargest(min(per_family_budget, len(group)), 'Rating Count')
        sampled_parts.append(take)
        print(f"Family '{family:<30}': {len(group):<5} perfumes, taking {len(take)}")
    
    sample_df = pd.concat(sampled_parts).reset_index(drop=True)

    # 7. Top up if we are under target
    shortfall = target - len(sample_df)
    if shortfall > 0:
        sampled_ids = set(sample_df['embedding_id'])
        remaining = df[~df['embedding_id'].isin(sampled_ids)]
        top_up = remaining.nlargest(shortfall, 'Rating Count')
        sample_df = pd.concat([sample_df, top_up]).reset_index(drop=True)
        print(f"Topping up with {len(top_up)} perfumes from remaining pool to reach target of {target}.")

    # 8. Shuffle and return
    return sample_df.sample(frac=1, random_state=42).reset_index(drop=True)