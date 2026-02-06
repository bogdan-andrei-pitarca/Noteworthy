import uvicorn
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import List, Dict, Any, Optional
import numpy as np
from ml_core.model_loader import get_ml_assets, load_ml_assets
from repository import fragrance_repo

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Noteworthy Fragrances API", version="1.0")

# CORS Middleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models

class FragranceRecord(BaseModel):
    embedding_id: int
    perfume_name: str
    brand: str
    gender: str
    launch_year: Optional[int]
    rating_value: Optional[float]
    rating_count: Optional[int]
    url: str
    main_accord_1: str
    main_accord_2: str
    main_accord_3: str
    main_accord_4: str
    main_accord_5: str
    all_notes: str
    similarity_percent: float

class SmellSearchResponse(BaseModel):
    query: str
    results: List[FragranceRecord]

# Startup event

@app.on_event("startup")
async def startup_event():
    # Load ML assets when the application starts
    logging.info("Loading ML assets on startup...")
    load_ml_assets()
    logging.info("FastAPI startup complete. ML assets loaded successfully.")

# Helper function for semantic search

def perform_semantic_search(query: str, k: int = 20) -> List[Dict[str, Any]]:
    """
    Performs semantic search using the FAISS index and SentenceTransformer model.

    :param query: Description
    :type query: str
    :param k: Description
    :type k: int
    :return: Description
    :rtype: List[Dict[str, Any]]
    """

    assets = get_ml_assets()
    faiss_index = assets.get('faiss_index')
    embedding_model = assets.get('embedding_model')

    if not faiss_index or not embedding_model:
        raise HTTPException(status_code=503, detail="AI services not fully initialized.")
    
    try:
        # 1. Encode the query text
        query_embedding = embedding_model.encode([query], convert_to_tensor=False).astype(np.float32)

        # 2. Perform FAISS search (D=Similarities, I=Indices/embedding_ids)
        D, I = faiss_index.search(query_embedding, k)

        search_results = []
        for idx, score in zip(I[0], D[0]):
            if idx < 0:
                continue  # Skip invalid indices
            search_results.append({
                'embedding_id': int(idx),
                'similarity_score': float(score)
            })
        
        # 3. Fetch fragrance details from the database
        embedding_ids = [res['embedding_id'] for res in search_results]
        db_records = fragrance_repo.get_fragrances_by_ids(embedding_ids)

        # 4. Merge similarity scores with database records
        final_results = []
        db_map = {rec['embedding_id']: rec for rec in db_records}

        for res in search_results:
            db_record = db_map.get(res['embedding_id'])
            if db_record:
                final_results.append({
                    **db_record,
                    'similarity_percent': round(res['similarity_score'] * 100, 2)  # Convert to percentage
                })
        return final_results
    except Exception as e:
        logging.error(f"Error during semantic search: {e}")
        raise HTTPException(status_code=500, detail="Error during semantic search.")

# API Endpoints

@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "Noteworthy Fragrances API is running."}

@app.get("/search/smell", response_model=SmellSearchResponse, tags=["AI Retrieval"])
async def search_by_smell(
    query: str = Query(..., min_length=3, description="Natural language description of the desired fragrance's characteristics."),
    k: int = Query(20, gt=0, le=100, description="Number of top similar fragrances to retrieve.")
):
    """
    Perform a semantic search for fragrances based on a textual description of smell characteristics.
    """
    logging.info(f"Received smell search query: {query} with top k={k}")
    results = perform_semantic_search(query, k)
    return {"query": query, "results": results}

@app.get("/search/notes_to_description", tags=["AI Generation"])
async def generate_description(
    notes: str = Query(..., description="List of fragrance notes to generate a description for.")
):
    """
    Endpoint for Fragrance Notes -> Natural Language Description.
    Uses the fine-tuned T5/BART generative model (currently placeholder).
    """
    assets = get_ml_assets()
    generator_model = assets.get('generator_model')
    generator_tokenizer = assets.get('generator_tokenizer')

    # TASK PREFIX FOR T5 FINE TUNING
    task_prefix = f"describe scent naturally: {notes}"

    inputs = generator_tokenizer(task_prefix, return_tensors="pt")
    outputs = generator_model.generate(**inputs, max_length=50, num_beams=4, early_stopping=True)
    description = generator_tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {"description": description}



if __name__ == "__main__":
    # Command to run the app: uvicorn main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)