import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os
import re
from typing import List

# Configuration of file paths
# Set BASE_DIR to the parent directory of `ml_core`, which is the `backend/` folder.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_CSV_PATH = os.path.join(DATA_DIR, 'fra_cleaned.csv')
FAISS_INDEX_PATH = os.path.join(DATA_DIR, 'fra_faiss_index.bin')
CLEAN_DATA_PATH = os.path.join(DATA_DIR, 'fra_data_processed.csv')
# DATA_WITH_DESC_PATH = os.path.join(DATA_DIR, 'fra_data_with_descriptions.csv')
# MODEL_PATH = os.path.join(BASE_DIR, 'fine_tuning', 'models', 'noteworthy_sbert_v1')
MODEL_PATH = 'all-MiniLM-L6-v2' 

def clean_and_normalize_data(df: pd.DataFrame) -> pd.DataFrame:
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
    df['Year_refined'] = df['Year'].apply(
        lambda y: f"released in {int(y)}" if not pd.isna(y) else "unknown"
    )

    # NORMALIZE AND COMBINE NOTES
    # def normalize_notes(notes_str: str) -> List[str]:
    #     """Splits, cleans and lowercases string of notes. May be redundant but ensures consistency."""
    #     notes_str = str(notes_str).replace(';', ',').replace('|', ',').replace(' and ', ',')
    #     notes = [n.strip().lower() for n in notes_str.split(',') if n.strip()]
    #     return notes

    def normalize_notes(notes):
        if pd.isna(notes):
            return "notes unknown"
        return str(notes).replace('[', '').replace(']', '').replace("'", "").replace('"', '')
    # this turns ['note1', 'note2'] into "note1, note2" 
    
    df['clean_notes'] = df['all_notes'].apply(normalize_notes)

    # CREATE UNIQUE EMBEDDING ID
    df.reset_index(drop=True, inplace=True)
    df['embedding_id'] = df.index

    print(f"Data cleaned: {len(df)} entries remaining after cleaning.")

    # create text input for sentence transformer
    df['embedding_text'] = df.apply(
        lambda row: (
            f"Fragrance: {row['Perfume']} by {row['Brand']}. "
            f"Target Gender: {row['Gender']}. "
            f"Vibe and Accords: {row['mainaccord1']}, {row['mainaccord2']}. "
            f"Technical Ingredient Notes: {row['clean_notes']}. "
            # f"Sensory AI Description: {row['t5_description']}."
        ),
        axis=1
    )

    # filter for output
    output_cols = ['embedding_id','url', 'Perfume', 'Brand', 'Gender', 'Year', 'Rating Value', 'Rating Count', 'all_notes', 'embedding_text']

    accord_cols = [c for c in df.columns if c.startswith('mainaccord')]

    final_cols = list(set(output_cols + accord_cols))
    final_cols = [c for c in final_cols if c in df.columns]

    return df[final_cols]

def create_embeddings_and_faiss_index(df: pd.DataFrame):
    """Generates embeddings and creates a FAISS index"""

    print("Loading fine-tuned SBERT model...")
    model = SentenceTransformer(MODEL_PATH)

    print("Generating embeddings...(may take a while)")
    embedding_texts = df['embedding_text'].tolist()
    fragrance_embeddings = model.encode(embedding_texts, show_progress_bar=True, convert_to_numpy=True)
    embeddings = np.array(fragrance_embeddings).astype('float32')

    print("Normalizing embeddings for Cosine Similarity...")
    faiss.normalize_L2(embeddings)

    print("Creating and populating FAISS index...")

    # We use IndexFlatIP for cosine similarity search (through inner product)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)

    print("Adding embeddings to FAISS index...")
    index.add(embeddings)

    print(f"Total embeddings in index: {index.ntotal}")
    print("Saving FAISS index to disk...")

    faiss.write_index(index, FAISS_INDEX_PATH)
    df.to_csv(CLEAN_DATA_PATH, index=False)

    print("FAISS index and cleaned data saved successfully.")
    
if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(CLEAN_DATA_PATH):
        raise FileNotFoundError(f"Data file not found at {CLEAN_DATA_PATH}. Please ensure the CSV file is present.")
    else:
        print("Loading raw data...")
        df = pd.read_csv(CLEAN_DATA_PATH, encoding='latin1')

        print("Cleaning and normalizing data...")
        cleaned_df = clean_and_normalize_data(df)

        print("Creating embeddings and FAISS index...")
        create_embeddings_and_faiss_index(cleaned_df)






