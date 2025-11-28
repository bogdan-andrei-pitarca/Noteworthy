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

def clean_and_normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalizes and combines data for embeddings"""

    REQUIRED_COLUMNS = ['Top', 'Middle', 'Base', 'Brand', 'Gender', 'mainaccord1', 'mainaccord2']

    df.dropna(subset=REQUIRED_COLUMNS, inplace=True)
    df.drop_duplicates(subset=['Perfume', 'Brand', 'Year'], inplace=True)
    
    # handling year data
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Year_refined'] = df['Year'].apply(
        lambda y: f"released in {int(y)}" if not pd.isna(y) else "unknown"
    )

    # NORMALIZE AND COMBINE NOTES
    def normalize_notes(notes_str: str) -> List[str]:
        """Splits, cleans and lowercases string of notes. May be redundant but ensures consistency."""
        notes_str = str(notes_str).replace(';', ',').replace('|', ',').replace(' and ', ',')
        notes = [n.strip().lower() for n in notes_str.split(',') if n.strip()]
        return notes
    
    # Process each notes column
    df['top_clean'] = df['Top'].apply(normalize_notes)
    df['middle_clean'] = df['Middle'].apply(normalize_notes)
    df['base_clean'] = df['Base'].apply(normalize_notes)

    # Combine all notes into a single list
    df['all_notes'] = df.apply(
        lambda row: row['top_clean'] + row['middle_clean'] + row['base_clean'], axis=1
    )

    # CREATE UNIQUE EMBEDDING ID
    df.reset_index(drop=True, inplace=True)
    df['embedding_id'] = df.index

    print(f"Data cleaned: {len(df)} entries remaining after cleaning.")

    # create text input for sentence transformer
    df['embedding_text'] = df.apply(
        lambda row: (
            f"{row['Perfume']} by {row['Brand']}, {row['Year_refined']}, "
            f"is a {row['Gender']} fragrance with the following accords: "
            f"{row['mainaccord1']}, {row['mainaccord2']}. "
            f"It features notes such as: {', '.join(row['all_notes'])}."
        ),
        axis=1
    )

    # filter for output
    df_output = df[['embedding_id','Perfume', 'Brand', 'Gender', 'Year', 'all_notes', 'embedding_text']]

    return df_output

def create_embeddings_and_faiss_index(df: pd.DataFrame):
    """Generates embeddings and creates a FAISS index"""

    print("Loading Sentence Transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Generating embeddings...(may take a while)")
    embedding_texts = df['embedding_text'].tolist()
    fragrance_embeddings = model.encode(embedding_texts, show_progress_bar=True, convert_to_numpy=True)
    embeddings = np.array(fragrance_embeddings).astype('float32')

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
    if not os.path.exists(RAW_CSV_PATH):
        raise FileNotFoundError(f"Raw data file not found at {RAW_CSV_PATH}. Please ensure the CSV file is present.")
    else:
        print("Loading raw data...")
        df_raw = pd.read_csv(RAW_CSV_PATH, encoding='latin1', sep=';')

        print("Cleaning and normalizing data...")
        cleaned_df = clean_and_normalize_data(df_raw)

        print("Creating embeddings and FAISS index...")
        create_embeddings_and_faiss_index(cleaned_df)






