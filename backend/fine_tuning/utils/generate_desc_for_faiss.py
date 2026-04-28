import os
import pandas as pd
import torch
from tqdm import tqdm
from transformers import T5ForConditionalGeneration, T5Tokenizer

# paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
INPUT_PATH = os.path.join(DATA_DIR, 'fra_data_processed.csv')
OUTPUT_PATH = os.path.join(DATA_DIR, 'fra_data_with_descriptions.csv')

# Use fine-tuned v3 model path
MODEL_PATH = os.path.join(BASE_DIR, 'fine_tuning', 'models', 'noteworthy_t5_v3')

BATCH_SIZE = 32

def bulk_generate():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"--- Using device: {device} ---")

    # 1. Load Model and Tokenizer
    print(f"Loading fine-tuned T5 from {MODEL_PATH}...")
    tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH).to(device)
    model.eval()

    # 2. Load Data
    df = pd.read_csv(INPUT_PATH)
    print(f"Loaded {len(df)} fragrances for processing.")

    descriptions = []

    # 3. Process in Batches for Speed
    # We iterate through the dataframe in chunks
    for i in tqdm(range(0, len(df), BATCH_SIZE), desc="Generating Descriptions"):
        batch_df = df.iloc[i : i + BATCH_SIZE]
        
        # Prepare inputs with the 'describe fragrance:' prefix
        inputs = [f"describe fragrance: {notes}" for notes in batch_df['all_notes'].tolist()]
        
        # Tokenize
        model_inputs = tokenizer(inputs, return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)

        # Generate
        with torch.no_grad():
            outputs = model.generate(
                **model_inputs,
                max_new_tokens=60,
                num_beams=4,
                no_repeat_ngram_size=2,
                repetition_penalty=1.5,
                early_stopping=True,
                forced_bos_token_id=tokenizer.encode("It")[0]
            )

        # Decode and clean
        decoded = [tokenizer.decode(o, skip_special_tokens=True) for o in outputs]
        descriptions.extend(decoded)

    # 4. Save the enriched dataset
    df['t5_description'] = descriptions
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"--- SUCCESS: Enriched data saved to {OUTPUT_PATH} ---")

if __name__ == "__main__":
    bulk_generate()