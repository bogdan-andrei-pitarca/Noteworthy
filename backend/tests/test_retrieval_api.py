import requests
import csv
import time
import os

API_URL = "http://127.0.0.1:8000/search/smell"

ENGINES = ['baseline', 'hybrid', 'sbert']

TEST_CASES = [
    # 1. Exact Lexical Matches
    "sweet tangy nectarines and vanilla",
    "dark smoky oud with rose",
    # 2. Pure Abstract / Vibe Checks
    "old dusty library books",
    "gasoline and hot rubber",
    "a walk through a damp pine forest in the rain",
    # 3. Misspellings / Typos
    "vnnilla and pchouli",
    "swet lether",
    # 4. Long Descriptive Paragraphs
    "I want to smell like a billionaire sitting in a leather chair smoking a Cuban cigar while drinking dark roasted coffee",
    # 5. Oxymorons / Contradictions
    "burning hot fire and freezing cold ice",
    "clean fresh laundry covered in dirty mud",
    # 6. Validation Check
    "ok"
]

def run_retrieval_tests():
    print("Starting Retrieval API Stress Test...\n")

    output_dir = os.path.join(os.path.dirname(__file__), "test_results")
    os.makedirs(output_dir, exist_ok=True)

    for engine_name in ENGINES:
        print(f"\n{'='*50}")
        print(f"ENGINE: {engine_name.upper()}")
        print(f"{'='*50}\n")

        results = []

        for i, query in enumerate(TEST_CASES, 1):
            print(f"[{i}/{len(TEST_CASES)}] '{query}'")

            payload = {"query": query, "k": 3, "engine": engine_name}
            start_time = time.time()

            try:
                response = requests.get(API_URL, params=payload)
                latency = round(time.time() - start_time, 2)

                if response.status_code in (400, 422):
                    detail = response.json().get('detail', 'Validation error')
                    print(f"    ↳ Expected HTTP {response.status_code}: {detail}")
                    results.append({
                        "engine": engine_name,
                        "query": query,
                        "rank_1": f"HTTP {response.status_code} (Expected)",
                        "rank_2": "-",
                        "rank_3": "-",
                        "latency_sec": latency
                    })
                    continue

                response.raise_for_status()
                data = response.json()
                returned_results = data.get("results", [])

                formatted_ranks = ["-", "-", "-"]
                for rank_idx, res in enumerate(returned_results[:3]):
                    name = res['perfume_name'].replace('-', ' ').title()
                    brand = res['brand'].replace('-', ' ').title()
                    score = res['similarity_percent']
                    formatted_ranks[rank_idx] = f"[{score}%] {name} by {brand}"
                    print(f"    ↳ Rank {rank_idx + 1}: {formatted_ranks[rank_idx]}")

                print(f"    ↳ Latency: {latency}s\n")

                results.append({
                    "engine": engine_name,
                    "query": query,
                    "rank_1": formatted_ranks[0],
                    "rank_2": formatted_ranks[1],
                    "rank_3": formatted_ranks[2],
                    "latency_sec": latency
                })

            except Exception as e:
                print(f"    ↳ Error: {e}\n")
                results.append({
                    "engine": engine_name,
                    "query": query,
                    "rank_1": f"ERROR: {str(e)}",
                    "rank_2": "-",
                    "rank_3": "-",
                    "latency_sec": round(time.time() - start_time, 2)
                })

        # one CSV per engine
        filename = f"retrieval_test_{engine_name}.csv"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["engine", "query", "rank_1", "rank_2", "rank_3", "latency_sec"]
            )
            writer.writeheader()
            writer.writerows(results)

        print(f"\nSaved: test_results/{filename}")

    print("\nAll engines tested.")

if __name__ == "__main__":
    run_retrieval_tests()