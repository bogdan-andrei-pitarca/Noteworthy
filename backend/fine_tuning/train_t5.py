import os
import pandas as pd
from datasets import Dataset
import evaluate
from transformers import T5Tokenizer, T5ForConditionalGeneration, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
import numpy as np
import nltk

# PATHS
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, 'datasets', 't5_golden_dataset_v2.csv')
MODEL_OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'noteworthy_t5_v1')

# download NLTK data for ROUGE evaluation
nltk.download('punkt_tab', quiet=True)
nltk.download('punkt', quiet=True)

def main():
    # LOAD DATA
    print ("--- Loading Golden Dataset... ---")
    df = pd.read_csv(DATA_PATH)

    # convert to huggingface dataset
    dataset = Dataset.from_pandas(df)

    # SPLIT INTO TRAIN/VAL
    print("--- Splitting into Train/Val ---")
    dataset = dataset.train_test_split(test_size=0.1, seed=42)

    # TOKENIZER AND MODEL
    print("--- Loading T5 Tokenizer and Model ---")
    model_name = 't5-small'  # can be 't5-base' or 't5-large' for better performance but more resource usage
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    # PREPROCESSING FUNCTION
    def preprocess_function(examples):
        # we add a task prefix to tell T5 what we want to do
        inputs = ["describe fragrance: " + notes for notes in examples['all_notes']] 
        model_inputs = tokenizer(inputs, text_target=examples["target_description"], max_length=128, truncation=True, padding='max_length') # add padding for batch processing
        # this is our study material 
        # columns for model_inputs are input_ids, attention_mask (list of 0s and 1s which separates true data from paddings), labels (which are the tokenized golden descriptions that the model will learn to generate)
        return model_inputs
    
    print("Tokenizing data...")
    tokenized_datasets = dataset.map(preprocess_function, batched=True)

    # METRICS (ROUGE-L)
    metric = evaluate.load('rouge')

    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
        # -100 is the default ignore index in hugging face. It means "ignore this token when calculating loss".
        # We replace it with the tokenizer's pad_token_id so that it can be decoded properly.
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

        # ROUGE expects a newline after each sentence
        decoded_preds = ["\n".join(nltk.sent_tokenize(pred.strip())) for pred in decoded_preds]
        decoded_labels = ["\n".join(nltk.sent_tokenize(label.strip())) for label in decoded_labels]

        result = metric.compute(predictions=decoded_preds, references=decoded_labels, use_stemmer=True) # use_stemmer to improve matching by reducing words to their root form
        # compares the generated description to the golden description
        
        # extract ROUGE-L score
        result = {key: value * 100 for key, value in result.items()}
        # rouge metric returns three scores (precision, recall, f1). We take the f1 score as the main metric for evaluation, and multiply by 100 to convert to percentage.
        return {k: round(v, 4) for k, v in result.items()}
    
    # TRAINING ARGUMENTS
    training_args = Seq2SeqTrainingArguments(
        output_dir=MODEL_OUTPUT_DIR,
        eval_strategy="epoch",
        learning_rate=5e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        weight_decay=0.01,
        save_total_limit=3,
        num_train_epochs=5,
        predict_with_generate=True, # this tells the trainer to actually generate descriptions during evaluation, so that we can compute ROUGE scores on the generated text instead of just the raw logits.
        logging_dir='./logs',
        use_cpu=True
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model) # dynamically pads inputs and labels to max length so they are all equal within a batch. required to perform matrix multiplication.

    # TRAINER
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
        eval_dataset=tokenized_datasets['test'],
        data_collator=data_collator,
        processing_class=tokenizer,
        compute_metrics=compute_metrics
    ) # takes all components and runs the forward and backward passes, calculates loss and logs the ROUGE-L scores at the end of every epoch.

    print("--- Starting Training ---")
    trainer.train()

    # SAVE THE MODEL
    print(f"--- Training complete! Saving model to {MODEL_OUTPUT_DIR} ---")
    trainer.save_model(MODEL_OUTPUT_DIR)
    tokenizer.save_pretrained(MODEL_OUTPUT_DIR)
    print("Model and tokenizer saved successfully.")

if __name__ == "__main__":
    main()