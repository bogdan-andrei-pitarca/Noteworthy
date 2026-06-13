import json
import logging
import asyncio
from functools import partial
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional
import math
from repository import fragrance_repo

class FragranceBase(BaseModel):
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

class FragranceSearchResult(FragranceBase):
    similarity_percent: float

class SmellSearchResponse(BaseModel):
    query: str
    results: List[FragranceSearchResult]
    current_page: int
    total_pages: int
    total_results: int

class ProfileRequest(BaseModel):
    favorite_ids: List[int]

# Initialize the router. Note we strip the "/search" prefix out of the @router.get paths below
router = APIRouter(prefix="/search", tags=["AI Retrieval & Generation"])

@router.get("/smell", response_model=SmellSearchResponse)
async def search_by_smell(
    request: Request,
    query: str = Query(..., min_length=3),
    page: int = Query(1, ge=1), # page nr
    page_size: int = Query(12, ge=1), # items per page
    engine: str = Query('sbert', pattern="^(baseline|hybrid|sbert)$")
):
    clean_query = query.strip().lower()
    predictor = request.app.state.predictor
    redis_client = request.app.state.redis_client

    cache_key = f"smell_search:{engine}:{page}:{page_size}:{clean_query}"
    
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
        # get top 60 results from FAISS
        MAX_RESULTS = 60
        all_results = predictor.perform_semantic_search(query, k=MAX_RESULTS, engine=engine)

        # calculate pagination
        total_results = len(all_results)
        total_pages = math.ceil(total_results / page_size)

        # slice the array for the current page
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_results = all_results[start_idx:end_idx]

        response_data = {
            "query": query,
            "results": paginated_results,
            "current_page": page,
            "total_pages": total_pages,
            "total_results": total_results
        }
        
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


@router.get("/details/{embedding_id}", response_model=FragranceBase)
async def get_fragrance_detail(embedding_id: int):
    """Fetch a single fragrance by its ID for the detail page."""
    records = fragrance_repo.get_fragrances_by_ids([embedding_id])
    if not records:
        raise HTTPException(status_code=404, detail="Fragrance not found.")
    return records[0]


@router.get("/similar/{embedding_id}", response_model=List[FragranceSearchResult])
async def get_similar_fragrances(request: Request, embedding_id: int, engine: str = 'sbert'):
    """Item-to-Item retrieval: Finds similar fragrances based on an existing fragrance's profile."""
    # fetch the target fragrance
    records = fragrance_repo.get_fragrances_by_ids([embedding_id])
    if not records:
        raise HTTPException(status_code=404, detail="Fragrance not found")
    
    frag = records[0]
    
    # build a rich semantic query using its notes and top accords
    query_text = f"{frag['all_notes']} {frag['main_accord_1']} {frag['main_accord_2']}"
    
    # perform standard semantic search
    predictor = request.app.state.predictor
    results = predictor.perform_semantic_search(query_text, k=6, engine=engine)
    
    # filter out the original fragrance and return the top 3 matches
    similar_fragrances = [r for r in results if r['embedding_id'] != embedding_id][:3]
    
    return similar_fragrances

@router.post("/profile/radar", tags=["User Profile"])
async def generate_scent_profile(request: ProfileRequest):
    """
    Generates a personal scent profile based on favorited perfumes.
    """
    if not request.favorite_ids:
        return []
    
    profile_data = fragrance_repo.get_user_scent_profile(request.favorite_ids)

    # max value, so we can scale the radar chart properly
    total_accords = sum(item['A'] for item in profile_data) if profile_data else 1

    # add a 'fullMark' key required by recharts to scale the radar web
    for item in profile_data:
        item['fullMark'] = profile_data[0]['A'] + 1 if profile_data else 10
        item['subject'] = item['subject'].capitalize()

    return profile_data
 
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