from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

model_path = r"D:\faculta\licenta\Noteworthy\backend\fine_tuning\models\noteworthy_t5_v3"

print("--- Loading noteworthy_t5_v3 ---")
tokenizer = T5Tokenizer.from_pretrained(model_path, legacy=False)
model = T5ForConditionalGeneration.from_pretrained(model_path)

# Move to CPU for local testing
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# A test input the model HAS NOT seen
test_notes = "['blood orange', 'vanilla', 'sandalwood', 'black pepper']"
input_text = f"describe fragrance: {test_notes}"

print(f"\nTesting notes: {test_notes}")

# Tokenize and Generate
inputs = tokenizer(input_text, return_tensors="pt").to(device)
outputs = model.generate(
    inputs.input_ids, 
    max_length=50, 
    num_beams=5, 
    early_stopping=True
)

description = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(f"\nMODEL OUTPUT: {description}")
print("\n--- Test Complete ---")