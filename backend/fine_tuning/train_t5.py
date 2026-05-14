import os
import pandas as pd
from datasets import Dataset
import evaluate
from transformers import T5Tokenizer, T5ForConditionalGeneration, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
import numpy as np
import nltk

# PATHS
# adapted for colab - in local, these are set in the utils files and imported into this one, but for better modularity and to avoid path issues in colab, I'm defining them directly here.
DATA_PATH = '/content/t5_golden_dataset_claude_v2.csv'
MODEL_OUTPUT_DIR = '/content/noteworthy_t5_v3'

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
    model_name = 't5-base'  # can be 't5-base' or 't5-large' for better performance but more resource usage
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
    rouge_metric = evaluate.load('rouge')
    bertscore_metric = evaluate.load('bertscore')

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

        rouge_result = rouge_metric.compute(predictions=decoded_preds, references=decoded_labels, use_stemmer=True) # use_stemmer to improve matching by reducing words to their root form
        # compares the generated description to the golden description
        
        bertscore_result = bertscore_metric.compute(predictions=decoded_preds, references=decoded_labels, lang='en') # computes BERTScore, which uses contextual embeddings to evaluate the quality of generated text. 
        # It gives us precision, recall, and F1 scores based on how well the generated description matches the golden description in terms of meaning, not just exact word overlap.

        return{
            # rouge scores x 100
            **{k: round(v * 100, 4) for k, v in rouge_result.items()},
            # bertscore - take the mean F1 across all examples
            'bertscore_f1': round(sum(bertscore_result['f1']) / len(bertscore_result['f1']) * 100, 4)
        }
    
    # TRAINING ARGUMENTS
    training_args = Seq2SeqTrainingArguments(
        output_dir=MODEL_OUTPUT_DIR,
        eval_strategy="epoch",
        learning_rate=5e-5,
        per_device_train_batch_size=16, # increased from 8 since colab can handle it
        per_device_eval_batch_size=16, # same 
        label_smoothing_factor=0.1, # helps prevent overfitting by making the model less confident in its predictions, which can improve generalization.
        weight_decay=0.01,
        save_total_limit=2, # reduced to save colab disk space
        num_train_epochs=5,
        predict_with_generate=True, # this tells the trainer to actually generate descriptions during evaluation, so that we can compute ROUGE scores on the generated text instead of just the raw logits.
        logging_dir='./logs',
        logging_steps=50
        # use_cpu=True
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
    # 1. Save the model weights and config
    trainer.save_model(MODEL_OUTPUT_DIR) 
    
    # 2. Save the tokenizer explicitly
    # Using the tokenizer object directly ensures all files are bundled
    tokenizer.save_pretrained(MODEL_OUTPUT_DIR)
    
    # 3. EXTRA SAFETY: Manually save the vocabulary (the .model file)
    # This specifically creates the spiece.model file T5 needs
    tokenizer.save_vocabulary(MODEL_OUTPUT_DIR)
    
    print("Model and tokenizer saved successfully.")

if __name__ == "__main__":
    main()