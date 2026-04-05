import requests
import csv
import time
import os

API_URL = "http://127.0.0.1:8000/search/notes_to_description"  


TEST_CASES = [
    # too few notes
    {"notes": "vanilla"},
    {"notes": "cedarwood"},
    
    # too many notes
    {"notes": "bergamot, lemon, black pepper, leather, tobacco, oud, rose, iris, patchouli, vetiver, oakmoss, amber, civet"},
    {"notes": "grapefruit, yuzu, mint, basil, lavender, rosemary, pine, cedar, sandalwood, musk, tonka bean, vanilla"},
    
    # contradictions
    {"notes": "aquatic sea salt, heavy dark smoke, sweet cotton candy"},
    {"notes": "icy mint, burning hot chili pepper, warm amber"},
    
    # absurd
    {"notes": "pepperoni pizza, motor oil, gasoline"},
    {"notes": "wet dog, old library books, copper coins"},
    
    # abstract
    {"notes": "solar notes, moonlight accord, stardust, frozen water"},
    
    # highly specific
    {"notes": "roasted coffee beans, dark chocolate, bitter almond, warm musk"}
]

def run_tests():
    print("Starting API Stress Test...\n")
    results = []

    for i, test in enumerate(TEST_CASES, 1):
        notes = test["notes"]
        print(f"[{i}/{len(TEST_CASES)}] Testing: {notes}")
        
        try:
            # Adjust the JSON payload key ('notes', 'query', etc.) to match what your API expects
            payload = {"notes": notes} 
            
            start_time = time.time()
            response = requests.get(API_URL, params=payload)
            response.raise_for_status()
            
            description = response.json().get("description", "ERROR: No description found") 
            latency = round(time.time() - start_time, 2)
            
            results.append({
                "input_notes": notes,
                "output": description,
                "latency_sec": latency
            })
            
            print(f"    ↳ Output: {description}")
            print(f"    ↳ Time: {latency}s\n")
            
        except Exception as e:
            print(f"Error: {e}\n")
            results.append({
                "input_notes": notes,
                "output": f"ERROR: {str(e)}",
                "latency_sec": 0
            })

    # save to csv
    filename = "generation_test_results.csv"
    output_dir = "test_results"
    filepath = os.path.join(os.path.dirname(__file__), output_dir, filename)
    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["input_notes", "output", "latency_sec"])
        writer.writeheader()
        writer.writerows(results)
        
    print(f"Testing complete! Results saved to {filename}")

if __name__ == "__main__":
    run_tests()