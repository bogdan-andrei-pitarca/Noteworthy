import torch
from typing import List
import re
import logging

BANNED_OUTPUT_PATTERNS = [
    r'\b(\w{3,})\w*\b(?:\s+\w+){0,3}\s+\1\w*\b', # bans phrases like smoky smoke, woody wood, etc.
]

OVERUSED_COMBINATIONS = [
    ('white flowers', 'powdery'),
    ('earthy', 'slightly sweet'),
    ('spice market', 'dawn'),
    ('flower shop', 'dawn'),
]


class FragrancePredictor:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def check_quality(self, description: str) -> bool:
        for pattern in BANNED_OUTPUT_PATTERNS:
            if re.search(pattern, description.lower()):
                return False
        if len(description.split()) < 8: # arbitrary minimum length check
            return False
        for w1, w2 in OVERUSED_COMBINATIONS:
            if w1 in description.lower() and w2 in description.lower():
                return False
        return True

    def generate_description(self, notes: str) -> str:
        # encapsulate logic for generating description from notes using the T5 model
        task_prefix = f"describe fragrance: {notes}"

        print(f"DEBUG: The model is seeing exactly this: |{task_prefix}|")

        # handle tokenization
        inputs = self.tokenizer(task_prefix, return_tensors="pt").to(self.device)

        # handle generation (hyperparameters)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=60,
                num_beams=4,
                no_repeat_ngram_size=2,
                repetition_penalty=1.5,
                early_stopping=True,
                forced_bos_token_id=self.tokenizer.encode("It")[0]
            )

        # decoding
        description = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # quality check
        if not self.check_quality(description):
            logging.warning(f"Low quality output detected, retrying...")
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=60,
                    do_sample=True,
                    temperature=0.8,
                    top_p=0.92,
                    repetition_penalty=1.5,
                    forced_bos_token_id=self.tokenizer.encode("It")[0]
                )
            description = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return description