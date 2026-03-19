import pandas as pd
import ollama
from tqdm import tqdm
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(os.path.dirname(__file__), 'datasets', 'missing_scents_todo.csv')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'datasets', 't5_new_batch.csv')

def generate_description(notes):
    # updated prompt for better, less repetitive descriptions 
    prompt = f"""
    Write a luxury, atmospheric description for a perfume based on these notes: {notes}.

    STRICT RULES:
    1. DO NOT start with "As the fragrance unfolds", "As the scent unfurls", or "This fragrance is".
    2. DO NOT use the words "sun-kissed", "garden", "breeze", or "stepping into".
    3. START the description with a mood, a texture, or a specific temperature 
    (e.g., "Sharp and cold," "Ink-dark and rooted," "Velvety and dense").
    4. Explain the interaction: e.g., how the '{notes[0]}' balances the '{notes[-1]}'.
    5. Keep it evocative.
    6. Max length: 50 words.
    """
    try:
        response = ollama.generate(model='llama3', prompt=prompt, options={'temperature': 0.9, 'top_p': 0.95})
        return response['response'].strip().replace('"', '')
    except Exception as e:
        print(f"Error generating description: {e}")
        return ""
    
def main():
    print("--- Starting Golden Dataset (RE)Generation ---")

    # Load data
    if not os.path.exists(DATA_PATH):
        print(f"Data file not found at {DATA_PATH}")
        return
    df = pd.read_csv(DATA_PATH)

    # 2. STRATIFIED SAMPLING (diversity math)
    # We want 1000 total. We group main_accord_1 into "buckets", to get different scent families.
    # We take the top perfumes (by rating_count, since they are more popular and better-documented) from within each family.
    # print("--- Performing Stratified Sampling ---")

    # # sort globally by rating first
    # df_sorted = df.sort_values(by='Rating Count', ascending=False)

    # # take up to 100 from each until we hit 1000 total
    # sample_df = df_sorted.groupby('mainaccord1', group_keys=False).apply(
    #     lambda x: x.head(min(len(x), 100)),
    #     include_groups=False
    # ).head(1000).copy()

    # print(f"Sampled {len(sample_df)} perfumes for description generation.")

    # 3. TEACHER-STUDENT DISTILLATION
    descriptions = []
    # tqdm for progress bar (QOL improvement)
    for notes in tqdm(df['all_notes'], desc="Regenerating Descriptions"):
        desc = generate_description(notes)
        descriptions.append(desc)

    # 4. SAVE TO CSV
    df['target_description'] = descriptions
    df[['all_notes', 'target_description']].to_csv(OUTPUT_PATH, index=False)

    print(f"\n Success! 1000 Golden Pairs saved to {OUTPUT_PATH}")
    print(f"Sample Result: {descriptions[0]}")

if __name__ == "__main__":
    main()