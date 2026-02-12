import pandas as pd
import ollama
from tqdm import tqdm
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'fra_data_processed.csv')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 't5_golden_dataset.csv')

def generate_description(notes):
    prompt = f"""
    Task: You are a fragrance storyteller. Convert these notes into a natural, vivid description.
    Tone: Evocative, sensory.
    Requirement: Write a single sentence that captures the "vibe" and smell of the fragrance for a regular person.
    Guidelines: Use clear, sensory words (e.g., 'fresh,' 'warm,' 'sun-drenched'). 
    Constraint: Avoid technical jargon like "sillage" or "linear." Do not use quotes. Do not mention "top, middle, or base notes" by name.

    Notes: {notes}

    Sentence:"""
    try:
        response = ollama.generate(model='llama3', prompt=prompt)
        return response['response'].strip().replace('"', '')
    except Exception as e:
        print(f"Error generating description: {e}")
        return ""
    
def main():
    print("--- Starting Golden Dataset Generation ---")

    # Load data
    if not os.path.exists(DATA_PATH):
        print(f"Data file not found at {DATA_PATH}")
        return
    df = pd.read_csv(DATA_PATH)

    # 2. STRATIFIED SAMPLING (diversity math)
    # We want 1000 total. We group main_accord_1 into "buckets", to get different scent families.
    # We take the top perfumes (by rating_count, since they are more popular and better-documented) from within each family.
    print("--- Performing Stratified Sampling ---")

    # sort globally by rating first
    df_sorted = df.sort_values(by='Rating Count', ascending=False)

    # take up to 100 from each until we hit 1000 total
    sample_df = df_sorted.groupby('mainaccord1', group_keys=False).apply(
        lambda x: x.head(min(len(x), 100)),
        include_groups=False
    ).head(1000).copy()

    print(f"Sampled {len(sample_df)} perfumes for description generation.")

    # 3. TEACHER-STUDENT DISTILLATION
    descriptions = []
    # tqdm for progress bar (QOL improvement)
    for notes in tqdm(sample_df['all_notes'], desc="Generating Descriptions"):
        desc = generate_description(notes)
        descriptions.append(desc)

    # 4. SAVE TO CSV
    sample_df['target_description'] = descriptions
    sample_df[['all_notes', 'target_description']].to_csv(OUTPUT_PATH, index=False)

    print(f"\n Success! 1000 Golden Pairs saved to {OUTPUT_PATH}")
    print(f"Sample Result: {descriptions[0]}")

if __name__ == "__main__":
    main()