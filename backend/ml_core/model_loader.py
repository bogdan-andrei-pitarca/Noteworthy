import faiss
import os
import logging
from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
FAISS_INDEX_PATH = os.path.join(DATA_DIR, 'fra_faiss_index.bin')

ml_assets: Dict[str, Any] = {}

def load_ml_assets():
    """
    Loads all necessary ML assets including the SentenceTransformer model and FAISS index.
    """
    global ml_assets

    # 1. Load FAISS index
    logging.info(f"Loading FAISS index from {FAISS_INDEX_PATH}")
    try:
        faiss_index = faiss.read_index(FAISS_INDEX_PATH)
        ml_assets['faiss_index'] = faiss_index
        logging.info("FAISS index loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load FAISS index: {e}")
        ml_assets['faiss_index'] = None

    # 2. Load SentenceTransformer model
    logging.info("Loading SentenceTransformer model 'all-MiniLM-L6-v2'")
    try:
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        ml_assets['embedding_model'] = embedding_model
        logging.info("SentenceTransformer model loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load SentenceTransformer model: {e}")
        ml_assets['embedding_model'] = None

    logging.info("Loading T5 generatie model 't5-small'")
    try:
        # T5-small for now. we upgrade to t5-base later
        ml_assets['generator_model'] = T5ForConditionalGeneration.from_pretrained('t5-small')
        ml_assets['generator_tokenizer'] = T5Tokenizer.from_pretrained('t5-small')
        logging.info("T5 model and tokenizer loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load T5 model/tokenizer: {e}")
        ml_assets['generator_model'] = None
        ml_assets['generator_tokenizer'] = None

    logging.info("ML assets loading complete.")

    return ml_assets

def get_ml_assets() -> Dict[str, Any]:
    """
    Returns the loaded ML assets.
    """
    global ml_assets
    if not ml_assets:
        logging.info("ML assets not loaded yet. Loading now...")
        load_ml_assets()
    return ml_assets