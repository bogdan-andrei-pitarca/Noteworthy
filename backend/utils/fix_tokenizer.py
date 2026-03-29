from transformers import T5Tokenizer

# Point this to your local model folder
model_path = r"D:\faculta\licenta\Noteworthy\backend\fine_tuning\models\noteworthy_t5_v2"

# Load the tokenizer using only the spiece.model file
tokenizer = T5Tokenizer.from_pretrained(model_path, legacy=False)

# Re-save it. This will write clean, correctly formatted JSON files.
tokenizer.save_pretrained(model_path)
print("Tokenizer JSON files repaired!")