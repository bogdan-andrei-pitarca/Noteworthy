import pandas as pd
import os
import sys
import torch
from evaluate import load
from tqdm import tqdm 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # add parent directory to path for imports

from ml_core.model_loader import load_ml_assets, get_ml_assets
from ml_core.predictor import FragrancePredictor

# paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLDEN_DATASET_PATH = os.path.join(BASE_DIR, 'fine_tuning', 'datasets', 'claude', 't5_golden_dataset_claude_v2.csv')
OUTPUT_EVAL_PATH = os.path.join(BASE_DIR, 'tests', 'test_results', 'quantitative_evaluation_results.csv')

def run_quantitative_eval(sample_size=100):
    # load assets
    print("Loading ML assets...")
    load_ml_assets()
    assets = get_ml_assets()
    
    predictor = FragrancePredictor(
        generator_model=assets.get('generator_model'), 
        generator_tokenizer=assets.get('generator_tokenizer'),
        embedding_models=assets.get('embedding_models'),
        faiss_indices=assets.get('faiss_indices')
    )

    # load dataset
    if not os.path.exists(GOLDEN_DATASET_PATH):
        print(f"Error: Golden dataset not found at {GOLDEN_DATASET_PATH}")
        return
    
    df = pd.read_csv(GOLDEN_DATASET_PATH).sample(n=sample_size, random_state=42)

    # predictions
    print("Generating predictions...")
    predictions = []
    references = df['target_description'].tolist()

    for notes in tqdm(df['all_notes'], desc="Generating..."):
        pred = predictor.generate_description(notes)
        predictions.append(pred)

    # compute metrics
    print("Computing metrics...")
    rouge_metric = load('rouge')
    bertscore_metric = load('bertscore')

    # COMPUTE ROUGE
    rouge_results = rouge_metric.compute(predictions=predictions, references=references, use_stemmer=True)

    # COMPUTE BERTSCORE
    bertscore_results = bertscore_metric.compute(predictions=predictions, references=references, lang='en', model_type='roberta-large')
    avg_bertscore_f1 = sum(bertscore_results['f1']) / len(bertscore_results['f1'])

    # print results
    print("\n--- Quantitative Evaluation Results ---")
    print("="*30)
    print(f"ROUGE-1: {rouge_results['rouge1']:.4f}")
    print(f"ROUGE-L: {rouge_results['rougeL']:.4f}")
    print(f"BERTScore F1: {avg_bertscore_f1:.4f}")
    print("="*30)

    # save results to CSV
    df['model_prediction'] = predictions
    os.makedirs(os.path.dirname(OUTPUT_EVAL_PATH), exist_ok=True)
    df.to_csv(OUTPUT_EVAL_PATH, index=False)
    print(f"Saved detailed results to {OUTPUT_EVAL_PATH}")

if __name__ == "__main__":
    run_quantitative_eval(sample_size=100)