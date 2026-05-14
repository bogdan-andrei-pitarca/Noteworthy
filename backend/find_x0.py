import numpy as np
from repository import fragrance_repo
from ml_core.model_loader import load_ml_assets, get_ml_assets
from ml_core.predictor import FragrancePredictor, ACCORD_KEYWORDS

def calculate_true_midpoint():
    load_ml_assets()
    assets = get_ml_assets()
    
    predictor = FragrancePredictor(
        generator_model=assets.get('generator_model'),
        generator_tokenizer=assets.get('generator_tokenizer'),
        embedding_models=assets.get('embedding_models'),
        faiss_indices=assets.get('faiss_indices')
    )
    
    # diverse queries covering vibe, technical, and mixed
    test_queries = [
        "sweet tangy nectarines", "old dusty library books", "fresh laundry and rain",
        "dark smoky oud", "vanilla and caramel dessert", "cut grass in the morning",
        "gasoline and hot rubber", "spicy cinnamon and clove", "ocean breeze",
        "powdery grandma soap", "sharp metallic smoke", "wet soil and pine needles",
        "leather jacket on a cold night", "rose and jasmine bouquet", "warm amber resin",
        "bergamot and cedar", "dark chocolate and coffee", "clean skin after shower"
    ]
    
    raw_hybrid_scores = []
    
    for query in test_queries:
        query_embedding = predictor.embedding_models['finetuned'].encode(
            [query], convert_to_tensor=False
        ).astype('float32')
        
        D, I = predictor.faiss_indices['sbert'].search(query_embedding, 10)
        
        # fetch actual DB records to compute real hybrid score
        embedding_ids = [int(idx) for idx in I[0] if idx >= 0]
        db_records = fragrance_repo.get_fragrances_by_ids(embedding_ids)
        db_map = {rec['embedding_id']: rec for rec in db_records}
        
        for idx, score in zip(I[0], D[0]):
            if idx < 0:
                continue
            db_record = db_map.get(int(idx))
            if not db_record:
                continue
            
            semantic = float(score)
            lexical = predictor._lexical_overlap(query, db_record)
            boost = predictor._get_accord_boost(query, db_record)
            
            raw_hybrid = (semantic * 0.75) + (lexical * 0.20) + ((boost - 1.0) * 0.05)
            raw_hybrid_scores.append(raw_hybrid)
            
    raw_hybrid_scores = sorted(raw_hybrid_scores)
    
    x0_40 = np.percentile(raw_hybrid_scores, 40)
    x0_35 = np.percentile(raw_hybrid_scores, 35)
    
    print(f"Distribution: min={min(raw_hybrid_scores):.3f}, "
          f"median={np.median(raw_hybrid_scores):.3f}, "
          f"max={max(raw_hybrid_scores):.3f}")
    print(f"x0 at 40th percentile: {x0_40:.3f}")
    print(f"x0 at 35th percentile: {x0_35:.3f}")
    print(f"Results below 0.20: {sum(1 for s in raw_hybrid_scores if s < 0.20)}/{len(raw_hybrid_scores)}")
    print(f"Results above 0.40: {sum(1 for s in raw_hybrid_scores if s > 0.40)}/{len(raw_hybrid_scores)}")

if __name__ == "__main__":
    calculate_true_midpoint()