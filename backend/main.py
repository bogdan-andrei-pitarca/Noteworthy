import uvicorn
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import List, Dict, Any, Optional
import numpy as np
import redis
from ml_core.model_loader import get_ml_assets, load_ml_assets
from repository import fragrance_repo

logging.basicConfig(level=logging.INFO)

try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True) # decode_responses=True for string values
    redis_client.ping() # test
    logging.info("Connected to Redis successfully.")
except redis.ConnectionError as e:
    logging.warning(f"Failed to connect to Redis: {e}")
    redis_client=None

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
    Uses the fine-tuned T5.
    Includes Redis caching to prevent redudant ML inferences.
    """
    assets = get_ml_assets()
    generator_model = assets.get('generator_model')
    generator_tokenizer = assets.get('generator_tokenizer')

    if generator_model is None or generator_tokenizer is None:
        raise HTTPException(
            status_code=503, 
            detail="T5 Model is not loaded. Check backend logs for path errors."
        )
    
    notes = sanitise_notes_input(notes)
    if len(notes) < 3:
        return {"description": "Please provide at least one fragrance note", "cached": False}
    
    # check Redis cache first
    # create unique key for redis (e.g. "notes_to_desc:note1,note2,note3")
    cache_key = f"notes_to_desc:{notes.lower()}"

    if redis_client:
        try:
            cached_description = redis_client.get(cache_key)
            if cached_description:
                logging.info(f"Cache hit for notes: {notes}")
                return {"description": cached_description, "cached": True}
        except Exception as e:
            logging.error(f"Error accessing Redis cache: {e}")

    # TASK PREFIX FOR T5 FINE TUNING
    logging.info(f"Cache miss for notes: {notes}. Generating description via T5...")
    task_prefix = f"describe fragrance: {notes}"

    inputs = generator_tokenizer(task_prefix, return_tensors="pt")
    outputs = generator_model.generate(
    **inputs,
    max_new_tokens=60,
    num_beams=4,
    no_repeat_ngram_size=2,
    repetition_penalty=1.3,
    early_stopping=True,
    forced_bos_token_id=generator_tokenizer.encode("It")[0]
    )
    description = generator_tokenizer.decode(outputs[0], skip_special_tokens=True)

    # save to cache
    if redis_client:
        try:
            # save result with TTL of 24 hours (86400 seconds)
            redis_client.setex(cache_key, 86400, description)
            logging.info(f"Saved description to cache for notes: {notes}")
        except Exception as e:
            logging.error(f"Error saving to Redis cache: {e}")

    return {"description": description, "cached": False}


def sanitise_notes_input(notes: str) -> str:
    """
    Sanitizes the input notes string by removing extra spaces and ensuring consistent formatting.
    """
    notes = notes.strip().strip(':').strip()
    # remove accidental prefix duplications
    if notes.lower().startswith("describe fragrance:"):
        notes = notes[len('describe fragrance:'):].strip()
    return notes



if __name__ == "__main__":
    # Command to run the app: uvicorn main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)