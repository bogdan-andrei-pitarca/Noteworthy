from sentence_transformers import SentenceTransformer, InputExample, losses
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from torch.utils.data import DataLoader
import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datasets', 'sbert', 'sbert_query_pairs.csv')
df = pd.read_csv(DATA_PATH)

train_df = df.sample(frac=0.9, random_state=42)
eval_df = df.drop(train_df.index)

# convert to sentence-transformers format
train_examples = [
    InputExample(texts=[row['anchor'], row['positive']]) 
    for _, row in train_df.iterrows()
]

model = SentenceTransformer('all-MiniLM-L6-v2')

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=64)

train_loss = losses.MultipleNegativesRankingLoss(model=model)

evaluator = EmbeddingSimilarityEvaluator(
    sentences1=eval_df['anchor'].tolist()[:200],
    sentences2=eval_df['positive'].tolist()[:200],
    scores=[1.0] * min(200, len(eval_df)),
    name='fragrance-eval'
)

print("Starting SBERT fine-tuning...")
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=3, # fewer epochs with better data > more epochs with noisy data
    warmup_steps=50,
    evaluator=evaluator,
    evaluation_steps=100,
    show_progress_bar=True,
    output_path='./models/noteworthy_sbert_v2'
)

print("SBERT fine-tuning complete! Model saved to ./models/noteworthy_sbert_v1")