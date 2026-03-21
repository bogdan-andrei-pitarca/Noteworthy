import pandas as pd
import ollama
from tqdm import tqdm
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(os.path.dirname(__file__), 'datasets', 't5_golden_dataset.csv')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'datasets', 't5_golden_dataset_v2.csv')

def generate_description(notes):
    # updated prompt for better, less repetitive descriptions 
    # V2: UPDATED AGAIN - avoid overly-luxurious or poetic language. focus on clear analogies. focus on making associations specific to the notes.
    prompt = f"""
    Task: Translate these technical perfume notes into a human-readable "vibe" using real-world analogies.
    Notes: {notes}

    STRICT RULES:
    1. NO POETRY: Avoid "velvety," "dense," "whispers," or "ensnares."
    2. SENSORY ANALOGIES: Compare the scent to things people know (e.g., household items, specific foods, weather, simple fragrance notes or locations).
    3. TONE: Helpful, intuitive, and grounded. Focus on clear, relatable analogies.
    4. DIVERSITY: Ensure the analogies are specific to THESE notes. Do not repeat the same analogies for different scents.
    5. LIMIT: Max 50 words.
    6. START: Begin directly with the description.
    7. NO PERFUMERY JARGON: Do not use "Start/Heart/Base" or "Top/Middle/Bottom notes." 
    8. NARRATIVE FLOW: Describe the scent as a transformation in one fluid paragraph. 
    9. THE HOOK: The first sentence must capture the "Main Character" of the smell.
    10. EXAMPLE STYLE: "Smells like a cold glass of gin and tonic that slowly warms into a bouquet of fresh roses, eventually settling into the dry, woody scent of an old cigar box."
    11. NO REPETITIVE CLOSINGS: Do not end every description with "skin," "lotion," or "clean laundry." 
    12. DIVERSE BASES: If the base notes are woody, compare it to a physical place (e.g., "a sawdust-covered workshop"). If they are resinous, think of "old church pews" or "burnt sugar."
    """
    try:
        response = ollama.generate(model='llama3', prompt=prompt, options={'temperature': 0.8, 'top_p': 0.95})
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