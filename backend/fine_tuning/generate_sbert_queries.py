import anthropic 
import pandas as pd
import json
import os 
import sys
import ast
from dotenv import load_dotenv
from uvicorn import main

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# paths

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'fra_data_with_descriptions.csv')
SBERT_DIR = os.path.join(BASE_DIR, 'fine_tuning', 'datasets', 'sbert')

# files

BATCH_JSONL = os.path.join(SBERT_DIR, 'query_batch_requests.jsonl')
BATCH_ID_FILE = os.path.join(SBERT_DIR, 'query_batch_id.txt')
OUTPUT_PATH = os.path.join(SBERT_DIR, 'sbert_query_pairs.csv')

SYSTEM_PROMPT = """You generate realistic search queries that a fragrance buyer might type.
Given a fragrance's notes and description, write 3 different natural language queries 
that would lead someone to search for this fragrance.

Rules:
- Queries should be 5-15 words
- Prefer sensory language, but occasionally include specific notes if natural (e.g., vanilla, oud, rose, leather)
- Vary the style: one mood-based, one object-based, one experience-based
- Never use the fragrance name or brand
- Return ONLY a JSON array of 3 strings, nothing else

Example output:
["warm cozy amber on a cold night", "smells like old books and leather", "dark smoky wood after rain"]"""

def prepare_batch():
    """Reads the DS, samples it, and creates the JSONL requests file."""
    print("Preparing batch requests...")
    df = pd.read_csv(DATA_PATH)

    # sample 500 fragrances stratified by mainaccord1
    sample = df.groupby(['mainaccord1', 'Gender'], group_keys=False).apply(
        lambda x: x.nlargest(min(10, len(x)), 'Rating Count')
    ).head(500)

    print(f"Sampled {len(sample)} fragrances for query generation.")
    
    os.makedirs(SBERT_DIR, exist_ok=True)

    requests = []
    for _, row in sample.iterrows():
        user_content = f"Notes: {row['all_notes']}\nDescription: {row.get('t5_description', 'not available')}"
        requests.append({
            "custom_id": f"query-{row['embedding_id']}",
            "params": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 150,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": user_content}]
            }
        })

    with open(BATCH_JSONL, 'w') as f:
        for req in requests:
            f.write(json.dumps(req) + '\n')
    
    print(f"Wrote {len(requests)} requests to {BATCH_JSONL}")

def submit_batch():
    """Reads the JSONL file and submits it to the Anthropic Batch API."""
    print("Submitting batch to Anthropic...")
    if not os.path.exists(BATCH_JSONL):
        print(f"Batch file {BATCH_JSONL} not found. Run 'prepare' first.")
        return

    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    requests = []
    with open(BATCH_JSONL, 'r') as f:
        for line in f:
            requests.append(json.loads(line))

    batch = client.messages.batches.create(requests=requests)

    with open(BATCH_ID_FILE, 'w') as f:
        f.write(batch.id)

    print(f"Batch submitted with ID {batch.id}. Check status with 'status' command.")


def check_status():
    """Polls the batch status and prints progress."""
    if not os.path.exists(BATCH_ID_FILE):
        print("No batch ID found. Did you submit the batch yet?")
        return
    
    with open(BATCH_ID_FILE, 'r') as f:
        batch_id = f.read().strip()

    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    batch = client.messages.batches.retrieve(batch_id)

    print(f"--- Batch Status ---")
    print(f"Batch ID: {batch_id}")
    print(f"Status: {batch.processing_status.upper()}")

    counts = batch.request_counts
    print(f"Progress: {counts.succeeded} succeeded | {counts.processing} processing | {counts.errored} errored")

    if batch.processing_status == "ended":
        print("\nBatch is complete! You can now run the 'retrieve' command.")

def retrieve_results():
    """Downloads completed batch results and builds the training CSV."""
    print("Retrieving batch results...")
    if not os.path.exists(BATCH_ID_FILE):
        print("No batch ID found. Did you submit the batch yet?")
        return
    
    with open(BATCH_ID_FILE, 'r') as f:
        batch_id = f.read().strip()

    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    # check its actually done
    batch = client.messages.batches.retrieve(batch_id)
    if batch.processing_status != "ended":
        print(f"Batch is not complete yet. Current status: {batch.processing_status.upper()}")
        return
    
    df = pd.read_csv(DATA_PATH)
    df_map = df.set_index('embedding_id').to_dict('index')

    pairs = []
    for result in client.messages.batches.results(batch_id):
        if result.result.type != "succeeded":
            print(f"Skipping request {result.request_id} with status {result.result.type}")
            continue

        # Process the successful result
        embedding_id = int(result.custom_id.replace('query-', ''))
        row = df_map.get(embedding_id)
        if not row:
            print(f"No data found for embedding_id {embedding_id}. Skipping.")
            continue

        try:
            # grab the raw text response from Claude
            raw_text = result.result.message.content[0].text
            
            # extract only the list part
            start_idx = raw_text.find('[')
            end_idx = raw_text.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                print(f"Skipping {embedding_id}: No array found. Raw text: {raw_text}")
                continue
                
            clean_json_str = raw_text[start_idx:end_idx]
            
            # 3. Parse the cleaned string
            queries = json.loads(clean_json_str)

            # 1. Parse the notes list (matching data_processing.py exactly)
            raw_notes = row.get('all_notes', '[]')
            notes_list = []
            try:
                notes_list = ast.literal_eval(str(raw_notes))
            except:
                notes_list = []

            top_notes = notes_list[:8] if notes_list else []

            # 2. Extract Accords
            accords = [str(row.get(f'mainaccord{i}', '')).replace('none', '').strip() for i in range(1, 4)]
            accords = [a for a in accords if a]

            # 3. Build dense semantic string
            embedding_text = f"Accords: {', '.join(accords)}. "
            embedding_text += f"Notes: {', '.join(top_notes)}. "

            if pd.notna(row.get('t5_description')):
                embedding_text += f"Profile: {row.get('t5_description')}."

            embedding_text = embedding_text.strip()

            for query in queries:
                pairs.append({'embedding_id': embedding_id, 'anchor': query.strip(), 'positive': embedding_text})

        except Exception as e:
            print(f"Error processing result for embedding_id {embedding_id}: {e}")
            continue

    pd.DataFrame(pairs).to_csv(OUTPUT_PATH, index=False)
    print(f"Retrieved {len(pairs)} query pairs and saved to {OUTPUT_PATH}")

def main():
    commands = {
        'prepare': prepare_batch,
        'submit': submit_batch,
        'status': check_status,
        'retrieve': retrieve_results
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print("Usage: python generate_sbert_queries.py [command]")
        print("Available commands: prepare, submit, status, retrieve")
        return

    commands[sys.argv[1]]()



if __name__ == "__main__":
    main()