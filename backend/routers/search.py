import json
import logging
import asyncio
from functools import partial
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional

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

# Initialize the router. Note we strip the "/search" prefix out of the @router.get paths below
router = APIRouter(prefix="/search", tags=["AI Retrieval & Generation"])

@router.get("/smell", response_model=SmellSearchResponse)
async def search_by_smell(
    request: Request,
    query: str = Query(..., min_length=3),
    k: int = Query(20, gt=0, le=100),
    engine: str = Query('sbert', pattern="^(baseline|hybrid|sbert)$")
):
    clean_query = query.strip().lower()
    predictor = request.app.state.predictor
    redis_client = request.app.state.redis_client

    cache_key = f"smell_search:{engine}:{k}:{clean_query}"
    
    if redis_client:
        try:
            cached_result = redis_client.get(cache_key)
            if cached_result:
                logging.info(f"Cache hit for query: '{clean_query}'")
                return json.loads(cached_result)
        except Exception as e:
            logging.error(f"Error accessing Redis cache: {e}")

    logging.info(f"Cache miss for query: '{clean_query}'. Computing via FAISS/SBERT...")
    try:
        results = predictor.perform_semantic_search(query, k=k, engine=engine)
        response_data = {"query": query, "results": results}
        
        if redis_client:
            redis_client.setex(cache_key, 86400, json.dumps(jsonable_encoder(response_data)))
                
        return response_data
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.get("/notes_to_description", tags=["AI Generation"])
async def generate_description(
    request: Request,
    notes: str = Query(..., description="List of fragrance notes to generate a description for.")
):
    """
    Endpoint for Fragrance Notes -> Natural Language Description.
    Uses the fine-tuned T5.
    Includes Redis caching to prevent redudant ML inferences.
    """
    predictor = request.app.state.predictor
    redis_client = request.app.state.redis_client

    if predictor.model is None:
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
    
    try:
        loop = asyncio.get_event_loop()
        description = await loop.run_in_executor(
            None, 
            partial(predictor.generate_description, notes)
        )
    except Exception as e:
        logging.error(f"Error during description generation: {e}")
        raise HTTPException(status_code=500, detail="Error during description generation.")

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
    Ensures the input exactly matches the ['note1', 'note2'] format 
    the model learned during training.
    """
    notes = notes.strip().strip(':').strip()

    if notes.lower().startswith("describe fragrance"):
        notes = notes[len("describe fragrance"):].strip()

    if notes.startswith("[") and notes.endswith("]"):
        return notes

    # This turns "lemon, neroli" -> ["lemon", "neroli"] -> "['lemon', 'neroli']"
    notes_list = [n.strip().lower() for n in notes.split(",") if n.strip()]
    return str(notes_list)