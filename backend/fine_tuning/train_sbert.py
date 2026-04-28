from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datasets', 'sbert', 'sbert_training_data.csv')
df = pd.read_csv(DATA_PATH)

# convert to sentence-transformers format
train_examples = [
    InputExample(texts=[row['anchor'], row['positive']]) 
    for _, row in df.iterrows()
]

model = SentenceTransformer('all-MiniLM-L6-v2')

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=32)

train_loss = losses.MultipleNegativesRankingLoss(model=model)

print("Starting SBERT fine-tuning...")
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=4,
    show_progress_bar=True,
    output_path='./models/noteworthy_sbert_v1'
)

print("SBERT fine-tuning complete! Model saved to ./models/noteworthy_sbert_v1")