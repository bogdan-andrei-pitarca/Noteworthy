import pandas as pd
import ollama
from tqdm import tqdm
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(os.path.dirname(__file__), 'datasets', 't5_golden_dataset.csv')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'datasets', 't5_golden_dataset_v4.csv')

def generate_description(notes):
    # updated prompt for better, less repetitive descriptions 
    # V2: UPDATED AGAIN - avoid overly-luxurious or poetic language. focus on clear analogies. focus on making associations specific to the notes.
    # V3: agressive against lists, overhaul to avoid AI-isms, more explicit rules. added example of correct style.
    # V4: tried to fix mode collapse - gave more non-deterministic mappings and increased temperature
    prompt = f"""
    Notes: {notes}

    Task: Describe what this fragrance smells like to a normal person.

    GOAL:
    Translate all notes into concrete, everyday smells.

    RULES:

    1. FORMAT:
    - One sentence (max 40 words)
    - Start with: "It smells like"

    2. FOCUS:
    - Describe only 3–5 dominant smells

    3. NO NOTE NAMES:
    - NEVER output original note names
    - ALWAYS translate into real-world smells

    4. CORE MAPPINGS:
    - patchouli → wet leaves, forest floor
    - amber → glue, warm plastic, tree sap
    - sandalwood → pencil shavings, dry wood
    - cedar → sawdust, dry wood
    - musk → skin, clean laundry
    - vetiver → damp soil, roots
    - incense → smoke, burnt wood
    - oud → burnt wood, smoky resin
    - aldehydes → soap, fizzy clean air

    5. FALLBACK (USE THIS WHEN UNKNOWN):

    - flowers → soap, shampoo, powder
    - fruits → juicy, tart, candy-like fruit
    - green → crushed leaves, cut grass
    - woods → sawdust, wooden boards
    - resin → glue, plastic, smoke
    - water → rain, wet air, metallic
    - sweet → sugar, caramel, cream
    - spice → pepper, dry heat

    IMPORTANT:
    - NEVER leave a note untranslated

    6. VARIATION (CRITICAL):
    - Avoid repeating the same phrases
    - Instead of repeating:
        "dry wood" → use: sawdust, pencil shavings, wooden boards
        "warm plastic" → use: glue, melted plastic
        "sweet" → use: sugar, caramel, candy

    7. STYLE:
    - No vague words (fresh, elegant, rich, complex)
    - No storytelling
    - Optional: describe progression (at first → then → finally)

    GOOD:
    It smells like citrus peel and soap at first, then rubber, smoke, and sawdust.

    BAD:
    It smells fresh and elegant
    It smells like patchouli and amber

    OUTPUT:
    Return ONLY the sentence.
    """
    try:
        response = ollama.generate(model='llama3', prompt=prompt, options={'temperature': 0.65, 'top_p': 0.9})
        return response['response'].strip().replace('"', '')
    except Exception as e:
        print(f"Error generating description: {e}")
        return ""
    
def clean_output(text):
    # remove everything before "It smells like"
    if "It smells like" in text:
        text = text[text.find("It smells like"):]
    
    # keep only first sentence
    text = text.split(".")[0] + "."
    
    return text.strip()
    
def main():
    print("--- Starting Golden Dataset (RE)Generation (V4) ---")

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
    for i, notes in enumerate(tqdm(df['all_notes'], desc="Regenerating Descriptions")):
        desc = clean_output(generate_description(notes))
        descriptions.append(desc)

        if i < 3:  # print the first few for sanity check
            print(f"\n--- Sample {i+1} ---")
            print(f"\nNotes: {notes}")
            print(f"Generated Description: {desc}\n" + "-"*30)

    # 4. SAVE TO CSV
    df['target_description'] = descriptions
    df[['all_notes', 'target_description']].to_csv(OUTPUT_PATH, index=False)

    print(f"\n Success! 1000 Golden Pairs saved to {OUTPUT_PATH}")
    print(f"Sample Result: {descriptions[0]}")

if __name__ == "__main__":
    main()