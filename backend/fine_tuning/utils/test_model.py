import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'noteworthy_t5_v1')

def test_model():
    print(f"--- Testing the fine-tuned T5 model from {MODEL_PATH} ---")

    # Load the fine-tuned model and tokenizer
    tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)

    # Sample input
    test_cases = [
        "sea salt, sage, grapefruit, seaweed", # fresh/aquatic
        "dark chocolate, truffle, vanilla, hazelnut", # gourmand/sweet
        "leather, tobacco, smoke, agarwood", #woody/masculine
        "lily of the valley, green apple, musk" # floral/fresh
    ]

    print("\n--- Generating descriptions for test cases ---")
    for notes in test_cases:
        # prepare input for T5
        input_text = f"describe fragrance: [{notes}]"

        # tokenize input
        inputs = tokenizer(input_text, return_tensors="pt", max_length=128, truncation=True, padding='max_length')

        # generate output
        # use beam search for better results
        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=60,
            num_beams=5, # explores multiple word paths to find the best description
            no_repeat_ngram_size=2, # prevents model from getting stuck in loops (fresh, fresh, fresh...)
            early_stopping=True # stops generation when it thinks it's done, rather than always going to max_length
        )

        # decode and print
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"T5 INPUT: {notes}")
        print(f"T5 OUTPUT: {result}")
        print("---")

if __name__ == "__main__":
    test_model()