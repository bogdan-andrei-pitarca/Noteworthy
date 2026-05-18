import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import redis
from ml_core.model_loader import get_ml_assets, load_ml_assets
from ml_core.predictor import FragrancePredictor

from routers import search, auth, favorites

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Noteworthy Fragrances API", version="1.0")

# --- Redis Setup ---
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    app.state.redis_client = redis_client # Attach to app state for routers to use
    logging.info("Connected to Redis successfully.")
except redis.ConnectionError as e:
    logging.warning(f"Failed to connect to Redis: {e}")
    app.state.redis_client = None

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount routers
app.include_router(search.router)
app.include_router(auth.router)
app.include_router(favorites.router)

@app.on_event("startup")
async def startup_event():
    logging.info("Loading ML assets on startup...")
    load_ml_assets()
    assets = get_ml_assets()
    app.state.predictor = FragrancePredictor(
        generator_model=assets.get('generator_model'),
        generator_tokenizer=assets.get('generator_tokenizer'),
        embedding_models=assets.get('embedding_models'),
        faiss_indices=assets.get('faiss_indices')
    )
    logging.info("FastAPI startup complete.")

@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "Noteworthy Fragrances API is running."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)