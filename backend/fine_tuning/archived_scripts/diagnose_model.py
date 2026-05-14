import os
from transformers import T5ForConditionalGeneration

model_path = r"D:\faculta\licenta\Noteworthy\backend\fine_tuning\models\noteworthy_t5_v3"

# 1. Check if the weight file actually exists
weight_file = os.path.join(model_path, "pytorch_model.bin")
if not os.path.exists(weight_file):
    # Check for safetensors version too
    weight_file = os.path.join(model_path, "model.safetensors")

if os.path.exists(weight_file):
    size_gb = os.path.getsize(weight_file) / (1024**3)
    print(f"Found weights file: {os.path.basename(weight_file)}")
    print(f"Size: {size_gb:.2f} GB (Should be ~0.8-1.1 GB)")
else:
    print("CRITICAL: No weight file found in the v3 folder!")

# 2. Try loading and checking if it's the base model
model = T5ForConditionalGeneration.from_pretrained(model_path)
print(f"✅ Model loaded from {model_path}")