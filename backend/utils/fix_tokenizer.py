from transformers import T5Tokenizer

model_path = r"D:\faculta\licenta\Noteworthy\backend\fine_tuning\models\noteworthy_t5_v3"

tokenizer = T5Tokenizer.from_pretrained("t5-base", legacy=False)

# writes spiece.model + json files
tokenizer.save_pretrained(model_path)
print("Done! spiece.model and tokenizer files saved.")