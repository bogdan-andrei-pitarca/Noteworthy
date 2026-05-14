import pandas as pd
import numpy as np
import shutil
from google.colab import files
from sentence_transformers import SentenceTransformer, InputExample, losses
from sentence_transformers.evaluation import TripletEvaluator
from torch.utils.data import DataLoader

df = pd.read_csv('/content/sbert_triplets.csv')

# leak-proof split by embedding_id
unique_ids = df['embedding_id'].unique()
np.random.seed(42)
train_ids = np.random.choice(unique_ids, size=int(len(unique_ids) * 0.9), replace=False)
train_set = set(train_ids)

train_df = df[df['embedding_id'].isin(train_set)]
eval_df = df[~df['embedding_id'].isin(train_set)]

print(f"Train: {len(train_df)} queries from {len(train_ids)} fragrances")
print(f"Eval: {len(eval_df)} queries from {len(unique_ids) - len(train_ids)} fragrances")

# triplet examples - anchor, positive, negative
# MNRL automatically detects the 3rd item as a hard negative!
train_examples = [
    InputExample(texts=[row['anchor'], row['positive'], row['negative']])
    for _, row in train_df.iterrows()
]

model = SentenceTransformer('all-mpnet-base-v2')
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=32)

# --- EXACT MODIFICATION HERE ---
# MultipleNegativesRankingLoss uses your hard negative AND 31 other in-batch negatives
train_loss = losses.MultipleNegativesRankingLoss(model=model)
# -------------------------------

# TripletEvaluator measures: is anchor closer to positive than negative?
evaluator = TripletEvaluator(
    anchors=eval_df['anchor'].tolist(),
    positives=eval_df['positive'].tolist(),
    negatives=eval_df['negative'].tolist(),
    name='fragrance-triplet-v3'
)

# run evaluator before training to get baseline score
print("\nBaseline (before fine-tuning):")
evaluator(model, output_path='.')

# Train the model
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=3,
    warmup_steps=100,
    evaluator=evaluator,
    evaluation_steps=50,
    show_progress_bar=True,
    output_path='./noteworthy_sbert_v5'
)

print("\nFinal evaluation:")
evaluator(model, output_path='.')

# --- ZIP AND DOWNLOAD LOGIC ---
print("\nZipping the model for download...")
# This creates a file named 'noteworthy_sbert_v5.zip' from the output folder
shutil.make_archive('noteworthy_sbert_v5', 'zip', './noteworthy_sbert_v5')

print("Downloading to your local machine...")
# Triggers the browser download in Google Colab
files.download('noteworthy_sbert_v5.zip')