import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os
import sys
from typing import List

# Configuration of file paths
# Set BASE_DIR to the parent directory of `ml_core`, which is the `backend/` folder.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

RAW_CSV_PATH = os.path.join(DATA_DIR, 'fra_cleaned.csv')

CLEAN_DATA_PATH = os.path.join(DATA_DIR, 'fra_data_processed.csv')
DATA_WITH_DESC_PATH = os.path.join(DATA_DIR, 'fra_data_with_descriptions.csv')

# MODEL_PATH = os.path.join(BASE_DIR, 'fine_tuning', 'models', 'noteworthy_sbert_v1')

# output index paths, one for each variant (baseline, hybrid, sbert)
FAISS_PATHS = {
    'baseline': os.path.join(DATA_DIR, 'fra_faiss_index_baseline.bin'),
    'hybrid': os.path.join(DATA_DIR, 'fra_faiss_index_hybrid.bin'),
    'sbert': os.path.join(DATA_DIR, 'fra_faiss_index_sbert.bin')
}

# SBERT model paths, one for each variant 
SBERT_MODELS = {
    'baseline': 'all-MiniLM-L6-v2',  # baseline uses the standard pre-trained model
    'hybrid': 'all-MiniLM-L6-v2',    # hybrid also uses the standard pre-trained model
    'sbert': os.path.join(BASE_DIR, 'fine_tuning', 'models', 'noteworthy_sbert_v2')  # sbert variant uses the fine-tuned model
}

# decides whether to include T5 descriptions
USE_T5 = {
    'baseline': False,
    'hybrid': True,
    'sbert': True,
}

def normalize_notes(notes):
    """Cleans brackets and quotes from the notes string"""
    if pd.isna(notes):
        return "notes unknown"
    return str(notes).replace('[', '').replace(']', '').replace("'", "").replace('"', '')

def clean_and_normalize_data(df: pd.DataFrame, include_t5: bool) -> pd.DataFrame:
    """Normalizes and combines data for embeddings"""

    REQUIRED_COLUMNS = ['url', 'Brand', 'Gender', 'Perfume', 'all_notes']

    # safeguard against empty lists
    df['mainaccord1'] = df['mainaccord1'].fillna('general')
    df['mainaccord2'] = df['mainaccord2'].fillna('balanced')
    df['Gender'] = df['Gender'].fillna('unisex')

    for i in range (1,6):
        df[f'mainaccord{i}'] = df[f'mainaccord{i}'].fillna('none').astype(str) 

    df.dropna(subset=REQUIRED_COLUMNS, inplace=True)
    df.drop_duplicates(subset=['Perfume', 'Brand'], inplace=True)
    
    # handling year data
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['clean_notes'] = df['all_notes'].apply(normalize_notes)

    # CREATE UNIQUE EMBEDDING ID
    df.reset_index(drop=True, inplace=True)
    df['embedding_id'] = df.index

    print(f"Data cleaned: {len(df)} entries remaining after cleaning.")

    def build_text(row):
        year = int(row['Year']) if pd.notna(row.get('Year')) and str(row['Year']) != 'nan' else None
        year_str = f", released {year}" if year else ""

        accord1 = str(row['mainaccord1']).replace('none', '').strip()
        accord2 = str(row['mainaccord2']).replace('none', '').strip()
        accords = ', '.join([a for a in [accord1, accord2] if a])

        gender = str(row['Gender']).lower().strip()

        text = (
            f"{row['Perfume']} by {row['Brand']}{year_str} is a {gender} fragrance. "
            f"It smells {accords}. "
            f"Notes: {row['clean_notes']}."
        )

        if include_t5 and 't5_description' in row and pd.notna(row.get('t5_description')):
            text += f" {row['t5_description']}"

        return text
    
    df['embedding_text'] = df.apply(build_text, axis=1)

    # filter for output
    output_cols = ['embedding_id','url', 'Perfume', 'Brand', 'Gender', 'Year', 'Rating Value', 'Rating Count', 'all_notes', 'embedding_text']

    accord_cols = [c for c in df.columns if c.startswith('mainaccord')]

    final_cols = list(set(output_cols + accord_cols))
    final_cols = [c for c in final_cols if c in df.columns]

    return df[final_cols]

def create_embeddings_and_faiss_index(df: pd.DataFrame, model_path: str, index_path: str):
    """Generates embeddings and creates a FAISS index"""

    print(f"Loading fine-tuned SBERT model from {model_path}...")
    model = SentenceTransformer(model_path)

    print("Generating embeddings...(may take a while)")
    embeddings = model.encode(
        df['embedding_text'].tolist(), 
        show_progress_bar=True, 
        convert_to_numpy=True
    ).astype('float32')

    print("Normalizing embeddings for Cosine Similarity...")
    faiss.normalize_L2(embeddings)

    print("Creating and populating FAISS index...")

    # We use IndexFlatIP for cosine similarity search (through inner product)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)

    print("Adding embeddings to FAISS index...")
    index.add(embeddings)

    print(f"Total embeddings in index: {index.ntotal}")
    print(f"Saving FAISS index to {index_path}...")

    faiss.write_index(index, index_path)
    df.to_csv(CLEAN_DATA_PATH, index=False)

    print("FAISS index and cleaned data saved successfully.")
    
if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in FAISS_PATHS:
        print(f"Usage: python {sys.argv[0]} [variant]")
        print("  baseline  → MiniLM, no T5 descriptions")
        print("  hybrid    → MiniLM + T5 descriptions")
        print("  sbert     → fine-tuned SBERT + T5 descriptions")
        sys.exit(1)
    
    variant = sys.argv[1]
    include_t5 = USE_T5[variant]
    model_path = SBERT_MODELS[variant]
    index_path = FAISS_PATHS[variant]

    print(f"\n=== Building variant: {variant.upper()} ===")
    print(f"  SBERT model: {model_path}")
    print(f"  T5 descriptions: {include_t5}")
    print(f"  Output index: {index_path}\n")

    # choose input data
    input_path = DATA_WITH_DESC_PATH if include_t5 else CLEAN_DATA_PATH

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input data not found at {input_path}. Please run the appropriate data preparation scripts first.")
    
    df = pd.read_csv(input_path)
    cleaned_df = clean_and_normalize_data(df, include_t5=include_t5)
    create_embeddings_and_faiss_index(cleaned_df, model_path=model_path, index_path=index_path)






