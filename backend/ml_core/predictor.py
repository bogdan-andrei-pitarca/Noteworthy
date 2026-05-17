import math

import torch
from typing import List
import re
import logging
import numpy as np

from repository import fragrance_repo

BANNED_OUTPUT_PATTERNS = [
    r'\b(\w{3,})\w*\b(?:\s+\w+){0,6}\s+\1\w*\b', 
]

OVERUSED_COMBINATIONS = [
    ('white flowers', 'powdery'),
    ('earthy', 'slightly sweet'),
    ('spice market', 'dawn'),
    ('flower shop', 'dawn'),
    ('at',  'dawn')
]

ACCORD_KEYWORDS = {
    'leather': ['leather', 'suede', 'animalic'],
    'smoky': ['smoky', 'smoke', 'tobacco', 'birch'],
    'woody': ['woody', 'wood', 'cedar', 'sandalwood', 'forest'],
    'fresh': ['fresh', 'clean', 'laundry', 'aquatic', 'marine'],
    'floral': ['floral', 'flower', 'rose', 'jasmine', 'bloom'],
    'sweet': ['sweet', 'vanilla', 'caramel', 'gourmand', 'candy'],
    'citrus': ['citrus', 'lemon', 'orange', 'bergamot', 'grapefruit'],
    'spicy': ['spicy', 'pepper', 'cinnamon', 'spice', 'warm spicy'],
    'earthy': ['earthy', 'dirt', 'soil', 'petrichor', 'mossy', 'mushroom'],
    'powdery': ['powdery', 'powder', 'talc', 'soft'],
    'oud': ['oud', 'agarwood', 'resin', 'incense'],
    'fruity': ['fruity', 'fruit', 'berry', 'peach', 'apple'],
    'aquatic': ['aquatic', 'ocean', 'sea', 'water', 'marine', 'salt'],
    'amber': ['amber', 'warm', 'resinous', 'balsamic'],
}

class FragrancePredictor:
    def __init__(self, generator_model, generator_tokenizer, embedding_models, faiss_indices):
        # generative assets (t5)
        self.model = generator_model
        self.tokenizer = generator_tokenizer
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.model:
            self.model.to(self.device)

        # retrieval assets (sbert + faiss)
        self.embedding_models = embedding_models
        self.faiss_indices = faiss_indices

    def check_quality(self, description: str, original_notes: str = "") -> bool:
        for pattern in BANNED_OUTPUT_PATTERNS:
            if re.search(pattern, description.lower()):
                return False
        if len(description.split()) < 8:
            return False
        for w1, w2 in OVERUSED_COMBINATIONS:
            if w1 in description.lower() and w2 in description.lower():
                return False
        
        # check for direct note name reproduction
        if original_notes:
            notes_list = [n.strip().lower() for n in original_notes.replace('[', '').replace(']', '').replace("'", "").split(',')]
            desc_lower = description.lower()
            # if more than 2 note names appear verbatim in the output, reject
            direct_matches = sum(1 for note in notes_list if len(note) > 4 and note in desc_lower)
            if direct_matches > 2:
                return False
        
        return True

    def generate_description(self, notes: str) -> str:
        # encapsulate logic for generating description from notes using the T5 model
        task_prefix = f"describe fragrance: {notes}"

        print(f"DEBUG: The model is seeing exactly this: |{task_prefix}|")

        # handle tokenization
        inputs = self.tokenizer(task_prefix, return_tensors="pt").to(self.device)

        # handle generation (hyperparameters)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=60,
                num_beams=4,
                no_repeat_ngram_size=2,
                repetition_penalty=1.4,
                early_stopping=True,
                forced_bos_token_id=self.tokenizer.encode("It")[0]
            )

        # decoding
        description = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # quality check
        if not self.check_quality(description, original_notes=notes):
            logging.warning(f"Low quality output detected, retrying...")
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=60,
                    do_sample=True,
                    temperature=0.8,
                    top_p=0.92,
                    repetition_penalty=1.5,
                    forced_bos_token_id=self.tokenizer.encode("It")[0]
                )
            description = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return description
    
    # retrieval logic 

    def _get_accord_boost(self, query: str, fragrance: dict) -> float:
        query_lower = query.lower()
        boost = 1.0
        fragrance_accords = [str(fragrance.get(f'main_accord_{i}', '')).lower() for i in range(1, 6)]

        for accord, keywords in ACCORD_KEYWORDS.items():
            if any(kw in query_lower for kw in keywords) and any(accord in fa for fa in fragrance_accords):
                boost += 0.15  # arbitrary boost value for each matching accord
        return min(boost, 1.5)  # cap boost at 50% to prevent runaway scores
    
    def _lexical_overlap(self, query: str, fragrance: dict) -> float:
        query_words = set(query.lower().replace(',', '').split())
        target_text = (
            str(fragrance.get('all_notes', '')) + ' ' +
            str(fragrance.get('main_accord_1', '')) + ' ' +
            str(fragrance.get('main_accord_2', ''))
        ).lower()
        fragrance_words = set(target_text.replace('[', '').replace(']', '').replace("'", "").replace(',', '').split())
        overlap = len(query_words.intersection(fragrance_words))
        return min(overlap / 4.0, 1.0)
    
    def _calibrate_score(self, raw_hybrid: float) -> float:
        """
        Maps raw hybrid score to a 0-100 UI percentage using a logistic sigmoid.
        
        Chosen because:
        1. Strictly monotonic — preserves FAISS rank order exactly
        2. Compresses the extremes gracefully (no result ever shows 0% or 100%)
        3. Tuned to V5's isotropic space where pure semantic scores peak ~0.52-0.55
        
        Parameters tuned empirically:
        - k=10: moderate slope, readable spread between results
        - x0=0.324: inflection point set after find_x0.py
        """
        k = 8.0
        x0 = 0.324
        calibrated = 100.0 / (1.0 + math.exp(-k * (raw_hybrid - x0)))
        return round(max(0.0, min(100.0, calibrated)), 2)
    
    def perform_semantic_search(self, query: str, k: int = 20, engine: str = 'sbert') -> List[dict[str, any]]:
        faiss_index = self.faiss_indices.get(engine)
        model_type = 'finetuned' if engine == 'sbert' else 'base'
        embedding_model = self.embedding_models.get(model_type)

        if not faiss_index or not embedding_model:
            raise ValueError(f"Engine {engine} not properly configured.")
        
        # encode query
        query_embedding = embedding_model.encode([query], convert_to_tensor=False).astype(np.float32)

        # faiss search
        D, I = faiss_index.search(query_embedding, k)

        search_results = []
        for idx, score in zip(I[0], D[0]):
            if idx >= 0:
                search_results.append({'embedding_id': int(idx), 'similarity_score': float(score)})

        embedding_ids = [res['embedding_id'] for res in search_results]
        db_records = fragrance_repo.get_fragrances_by_ids(embedding_ids)
        db_map = {rec['embedding_id']: rec for rec in db_records}

        # hybrid scoring & calibration
        final_results = []
        for res in search_results:
            db_record = db_map.get(res['embedding_id'])
            if db_record:
                semantic_score = float(res['similarity_score'])
                lexical_score = self._lexical_overlap(query, db_record)
                accord_boost = self._get_accord_boost(query, db_record)

                raw_hybrid_score = (semantic_score * 0.75) + (lexical_score * 0.20) + ((accord_boost - 1.0) * 0.05)

                final_ui_percentage = self._calibrate_score(raw_hybrid_score)

                final_results.append({
                    **db_record,
                    'similarity_percent': round(final_ui_percentage, 2)
                })

        final_results.sort(key=lambda x: x['similarity_percent'], reverse=True)
        return final_results[:k]
