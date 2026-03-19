# we need to find the missing scents to regenerate
import pandas as pd
import os

# PATHS
# script is in fine_tuning/utils  
UTILS_DIR = os.path.dirname(os.path.abspath(__file__)) # define this for better scalability and path handling
# base is fine_tuning
BASE_DIR = os.path.dirname(UTILS_DIR)

MASTER_PATH = os.path.join(BASE_DIR, 'datasets', 't5_golden_dataset.csv')
CLEANED_PATH = os.path.join(BASE_DIR, 'datasets', 't5_golden_dataset_cleaned.csv')
TODO_PATH = os.path.join(BASE_DIR, 'datasets', 'missing_scents_todo.csv')

def find_missing():
    # load data
    if not os.path.exists(MASTER_PATH) or not os.path.exists(CLEANED_PATH):
        print("Error: Master or cleaned dataset not found. Please run the previous steps first.")
        return
    
    df_master = pd.read_csv(MASTER_PATH)
    df_cleaned = pd.read_csv(CLEANED_PATH)

    # identify missing
    # the idea is we find rows in master that are not in cleaned, based on "all_notes" (the unique identifier for each scent)
    missing_notes = df_master[~df_master['all_notes'].isin(df_cleaned['all_notes'])]

    print(f"Master List: {len(df_master)} rows")
    print(f"Cleaned List: {len(df_cleaned)} rows")
    print(f"Missing notes to regenerate: {len(missing_notes)} rows")

    # save the todo list (just the notes, so llama3 knows what to describe)
    missing_notes[['all_notes']].to_csv(TODO_PATH, index=False)
    print(f"Missing scents saved to {TODO_PATH}")

if __name__ == "__main__":
    find_missing()