"""
Uses Claude Sonnet 3.5 w/ BATCH API as the TEACHER model.
It has a more detailed prompt and more aggressive anti-AI-ism rules to try to fix the issues we had with the first version
 (overly poetic, repetitive, and AI-istic descriptions that didn't really capture the notes in a concrete way).

 Usages:

 1. python generate_claude_training_data.py prepare -> 
 reads t5_sample_stratified.csv, builds batch_requests.jsonl 
 2. python generate_claude_training_data.py submit -> submits the batch to Claude and saves the results
 3. python generate_claude_training_data.py status -> checks batch status (run every few minutes)
 4. python generate_claude_training_data.py retrieve -> download results, match each result back to its row using embedding_id and build golden dataset 

"""

import anthropic
import pandas as pd
import json
import os
import sys
import logging
from dotenv import load_dotenv

# CONFIG
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')) 

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(SCRIPT_DIR, 'datasets')
CLAUDE_DIR = os.path.join(DATASETS_DIR, 'claude')

INPUT_PATH = os.path.join(DATASETS_DIR, 't5_golden_regenerate.csv') # temp change to t5_golden_regenerate.csv after we clean the dataset and identify which rows to regenerate
BATCH_JSONL = os.path.join(CLAUDE_DIR, 'batch_requests.jsonl')
BATCH_ID_FILE = os.path.join(CLAUDE_DIR, 'batch_id.txt')
RESULTS_JSONL = os.path.join(CLAUDE_DIR, 'batch_results.jsonl')
OUTPUT_PATH = os.path.join(CLAUDE_DIR, 't5_golden_dataset_claude.csv')

MODEL = "claude-sonnet-4-5-20250929"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SYSTEM_PROMPT = """You translate perfume note lists into one-sentence smell descriptions for normal people.

OUTPUT FORMAT:
- Exactly one sentence starting with "It smells like"
- Maximum 35 words
- Never name the original notes
- Describe 3-5 dominant smells only

BANNED PHRASES — never use these:
- walking past, walking through, walking into
- where someone, someone just
- forest floor, warm skin, lemon candy, pencil shavings
- hint of, mixed with

BANNED STRUCTURES — never use these sentence patterns:
- "It smells like [place] where someone [verb]ed [thing]"
- "It smells like being in [place]"
- Any sentence requiring more than one scene or location

REQUIRED: describe the actual smell directly. Not a scene. Not a story.
Write what your nose detects, not what your eyes see.

GOOD EXAMPLES:
- "It smells like Earl Grey tea and citrus rind at first, then dry wood and something faintly smoky."
- "It smells like rose water, powdered sugar, and the inside of an old wooden box."
- "It smells like sunscreen, white flowers, and the sweet-sticky residue of tropical fruit."
- "It smells like burnt resin, dark leather, and the bitter edge of espresso."
- "It smells like cold stone, wet earth roots, and a faintly medicinal powder."

BAD EXAMPLES (do not write like this):
- "It smells like walking past a flower shop where someone just drizzled honey..."
- "It smells like a spice cabinet in an old library where someone peeled oranges..."

VARY YOUR STRUCTURE — use different patterns each time:
- "It smells like X and Y, with Z underneath."
- "It smells like X — dry and slightly Z, with a base of Y."
- "It smells like X at first, then Y, finishing with Z."
- "It smells like X, slightly Z, with a background of Y."

OUTPUT: Return only the sentence. No explanation."""


def build_user_prompt(notes: str) -> str:
    return f"{notes}\n\nDescribe what this fragrance smells like to a normal person."

def prepare_batch():
    """
    Reads the stratified CSV and writes a .jsonl file.
    JSONL is what Anthropic expects. Each line is an API request with a unique custom_id.
    """
    if not os.path.exists(INPUT_PATH):
        logging.error(f"Input file not found at {INPUT_PATH}. Please prepare the data first.")
        return
    
    df = pd.read_csv(INPUT_PATH)
    logging.info(f"Loaded {len(df)} rows from {INPUT_PATH}")

    os.makedirs(CLAUDE_DIR, exist_ok=True)

    with open(BATCH_JSONL, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            request = {
                "custom_id": f"frag-{row['embedding_id']}",
                "params": {
                    "model": MODEL,
                    "max_tokens": 100,
                    "system": SYSTEM_PROMPT,
                    "messages": [
                        {
                            "role": "user",
                            "content": build_user_prompt(str(row['all_notes']))
                        }
                    ]
                }
            }
            f.write(json.dumps(request) + '\n')

    logging.info(f"Batch requests written to {BATCH_JSONL}. Wrote {len(df)} requests.")

    logging.info("------ First 3 requests (sanity check) ------")
    with open(BATCH_JSONL, 'r') as f:
        for i, line in enumerate(f):
            if i >= 3:
                break
            req = json.loads(line)
            print(f"\nRequest {i+1}:")
            print(f"    ID:{req['custom_id']}:")
            print(f"    Notes:{req['params']['messages'][0]['content'][:120]}...")

    print(f"\nTotal requests prepared: {len(df)}")
    print(f"Estimated cost: ~${len(df) * 0.00225 / 2:.2f}")


def submit_batch():
    """
    Reads the JSONL file and submits to Anthropic (w/ Batch API)
    
    Anthropic validates => returns a batch object. batch_id is the metric by which we track the batch through the system. we save it to disk.
    """

    if not os.path.exists(BATCH_JSONL):
        logging.error(f"Batch request file not found at {BATCH_JSONL}. Please prepare the batch first.")
        return
    
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    logging.info("Submitting batch to Anthropic...")

    # read all requests into a list
    # batch.create() expects a list
    requests = []
    with open(BATCH_JSONL, 'r', encoding='utf-8') as f:
        for line in f:
            requests.append(json.loads(line))

    logging.info(f"Submitting {len(requests)} requests in batch...")

    batch = client.messages.batches.create(requests=requests)

    batch_id = batch.id
    logging.info(f"Batch submitted successfully. Batch ID: {batch_id}")
    logging.info(f"Batch status: {batch.processing_status}")

    with open(BATCH_ID_FILE, 'w') as f:
        f.write(batch_id)

    logging.info(f"Batch ID saved to {BATCH_ID_FILE}")


def check_status():
    """
    Polls Anthropic with batch_id and prints the current state

    Possible statuses:
    - in_progress
    - ended
    - canceling 
    - expired

    Run every few minutes until "ended".
    """

    if not os.path.exists(BATCH_ID_FILE):
        logging.error(f"Batch ID file not found at {BATCH_ID_FILE}. Please submit a batch first.")
        return
    
    with open(BATCH_ID_FILE, 'r') as f:
        batch_id = f.read().strip()

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    batch = client.messages.batches.retrieve(batch_id)

    print(f"Batch ID: {batch_id}")
    print(f"Batch status: {batch.processing_status}")

    counts = batch.request_counts
    print(f"Processing: {counts.processing}, Succeeded: {counts.succeeded}, Errored: {counts.errored}, Canceled: {counts.canceled}, Expired: {counts.expired}")

    if batch.processing_status == "ended":
        print("Batch processing complete! You can now retrieve results.")


def retrieve_results():
    """
    Downloads results and build final training CSV.
    """

    if not os.path.exists(BATCH_ID_FILE):
        logging.error(f"Batch ID file not found at {BATCH_ID_FILE}. Please submit a batch first.")
        return
    
    with open(BATCH_ID_FILE, 'r') as f:
        batch_id = f.read().strip()

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    batch = client.messages.batches.retrieve(batch_id)
    if batch.processing_status != "ended":
        logging.error(f"Batch is not yet complete. Current status: {batch.processing_status}. Please check again later.")
        return
    
    logging.info(f"Retrieving results for batch ID: {batch_id}...")

    # each obj has a custom_id (which we set to "frag-{embedding_id}") and a response (the generated description)

    descriptions = {}
    errors = []

    for result in client.messages.batches.results(batch_id):
        custom_id = result.custom_id
        
        # parse custom_id to get embedding_id

        try:
            embedding_id = int(custom_id.replace("frag-", ""))
        except ValueError:
            logging.warning(f"Unexpected custom_id format: {custom_id}. Skipping.")
            continue

        if result.result.type == "succeeded":

            # text is first content block
            text = result.result.message.content[0].text.strip() 

            if "It smells like" in text:
                text = text[text.find("It smells like"):]
            text = text.split(".")[0] + "."

            descriptions[embedding_id] = text

        else:
            logging.warning(f"Request with custom_id {custom_id} failed with error: {result.result.error}")
            errors.append(custom_id)
    
    logging.info(f"Retrieved {len(descriptions)} descriptions. {len(errors)} errors.")

    if errors:
        logging.warning(f"Failed requests: {errors}")

    df = pd.read_csv(INPUT_PATH)
    df['target_description'] = df['embedding_id'].map(descriptions)

    missing = df['target_description'].isna().sum()
    if missing > 0:
        logging.warning(f"{missing} descriptions are missing due to failed requests. They will be dropped from the final dataset.")
        df = df.dropna(subset=['target_description'])

    # t5 only needs all_notes and target_description
    # we keep mainaccord1 to audit for family distribution

    output_df = df[['embedding_id', 'all_notes', 'mainaccord1', 'target_description']]
    output_df.to_csv(OUTPUT_PATH, index=False)

    logging.info(f"Final dataset with {len(output_df)} rows saved to {OUTPUT_PATH}")

    print("\n---Sample outputs (first 5 rows)---")
    for _, row in output_df.head(5).iterrows():
        print(f"\nNotes: {str(row['all_notes'])[:80]}...")
        print(f"Main Accord: {row['mainaccord1']}")
        print(f"Generated Description: {row['target_description']}")

    print("Done!!")


def main():
    commands = {
        "prepare": prepare_batch,
        "submit": submit_batch,
        "status": check_status,
        "retrieve": retrieve_results
    }

    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        print("Usage: python generate_claude_training_data.py [command]")
        print("Commands:")
        for cmd in commands:
            print(f"  {cmd}")
        return
    
    commands[sys.argv[1]]()

if __name__ == "__main__":
    main()