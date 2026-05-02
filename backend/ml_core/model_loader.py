import faiss
import os
import logging
from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)
load_dotenv()  # Load environment variables from .env file

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
DATA_DIR = os.path.join(BASE_DIR, 'data')
FT_MODEL_PATH = os.path.join(BASE_DIR, 'fine_tuning', 'models', 'noteworthy_t5_v3') # PATH TO MODEL - CHANGE IF UPDATED

FAISS_INDEX_PATHS = {
    'baseline': os.path.join(DATA_DIR, 'fra_faiss_index_baseline.bin'),
    'hybrid': os.path.join(DATA_DIR, 'fra_faiss_index_hybrid.bin'),
    'sbert': os.path.join(DATA_DIR, 'fra_faiss_index_sbert.bin')
}

SBERT_MODEL_PATHS = {
    'base': 'all-mpnet-base-v2',  # baseline uses the standard pre-trained model
    'finetuned': os.path.join(BASE_DIR, 'fine_tuning', 'models', 'noteworthy_sbert_v3')  # sbert variant uses the fine-tuned model
}

ml_assets: Dict[str, Any] = {
    'faiss_indices': {},
    'embedding_models': {}
}

def load_ml_assets():
    """
    Loads all necessary ML assets including the SentenceTransformer model and FAISS index.
    """
    global ml_assets

    for mode, path in FAISS_INDEX_PATHS.items():
        logging.info(f"Loading {mode.upper()} FAISS index from {path}")
        try:
            if os.path.exists(path):
                ml_assets['faiss_indices'][mode] = faiss.read_index(path)
                logging.info(f"{mode.upper()} FAISS index loaded successfully.")
            else:
                logging.warning(f"Index {path} not found. Skipping {mode}.")
        except Exception as e:
            logging.error(f"Failed to load {mode.upper()} FAISS index: {e}")
            ml_assets['faiss_indices'][mode] = None

    for m_type, path in SBERT_MODEL_PATHS.items():
        logging.info(f"Loading {m_type.upper()} SBERT model from {path}")
        try:
            ml_assets['embedding_models'][m_type] = SentenceTransformer(path)
        except Exception as e:
            logging.error(f"Failed to load {m_type} SBERT model: {e}")
            ml_assets['embedding_models'][m_type] = None

    logging.info("Loading T5 generative model 't5-base'")
    try:
        # T5-small for now. we upgrade to t5-base later
        # UPGRADED BY MAR. 29: T5-base for better performance. 
        if not os.path.exists(FT_MODEL_PATH):
            logging.error(f"Model path does not exist: {FT_MODEL_PATH}") 

        print(f"Attempting to load T5 model from: {FT_MODEL_PATH}")

        model_path = str(Path(FT_MODEL_PATH).resolve())
        logging.info(f"Resolved model path: {model_path}")

        ml_assets['generator_model'] = T5ForConditionalGeneration.from_pretrained(
            model_path, local_files_only=True
        )
        ml_assets['generator_tokenizer'] = T5Tokenizer.from_pretrained(
            model_path, local_files_only=True
        )
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