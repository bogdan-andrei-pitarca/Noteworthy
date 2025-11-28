# test that the FAISS index works

import os
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
FAISS_INDEX_PATH = os.path.join(DATA_DIR, 'fra_faiss_index.bin')
CLEAN_DATA_PATH = os.path.join(DATA_DIR, 'fra_data_processed.csv')

def test_faiss_index():
    """Loads the FAISS index and performs a sample semantic search."""

    # 1. Load the ML Assets
    print("Loading FAISS Index...")
    try:
        index = faiss.read_index(FAISS_INDEX_PATH)
    except Exception as e:
        print(f"ERROR: Could not load FAISS index. Please re-run data_processing.py. Error: {e}")
        return

    print(f"Total indexed vectors: {index.ntotal}")

    print("Loading Sentence Transformer...")
    # Must use the exact same model used for generating the embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2') 

    print("Loading Cleaned DataFrame for Result Lookup...")
    df_clean = pd.read_csv(CLEAN_DATA_PATH)
    
    # 2. Define a Test Query
    query_text = "A light, slightly sweet citrus scent with soft white florals."
    k = 5 # Number of nearest neighbors to retrieve

    print(f"\n--- Testing Semantic Search ---")
    print(f"Query: '{query_text}'")

    # 3. Encode the Query
    query_vector = model.encode([query_text], convert_to_tensor=False).astype('float32')

    # 4. Perform the Search
    # D = Distances (Similarities), I = Indices (The embedding_id)
    D, I = index.search(query_vector, k) 

    print(f"Found {k} nearest neighbors.")

    # 5. Interpret Results
    search_indices = I[0] # The list of IDs found by FAISS
    similarity_scores = D[0] # The list of similarity scores (Inner Product)
    
    results = []
    for rank, (idx, score) in enumerate(zip(search_indices, similarity_scores)):
        # Retrieve the structured data from the clean DataFrame using the index ID
        fragrance_row = df_clean[df_clean['embedding_id'] == idx].iloc[0]
        
        results.append({
            "Rank": rank + 1,
            "Perfume": fragrance_row['Perfume'],
            "Brand": fragrance_row['Brand'],
            "Similarity (%)": round(float(score) * 100, 2), # Convert score to percentage
            "Notes (Sample)": ', '.join(eval(fragrance_row['all_notes']))[:60] + "...",
        })

    # Display results
    results_df = pd.DataFrame(results)
    print("\nSearch Results (Top 5 Matches):")
    print(results_df.to_markdown(index=False))

if __name__ == "__main__":
    test_faiss_index()