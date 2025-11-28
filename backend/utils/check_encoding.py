import chardet
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_CSV_PATH = os.path.join(DATA_DIR, 'fra_cleaned.csv')

def detect_file_encoding(file_path: str, num_bytes: int = 24063) -> str:
    """Detects the encoding of a file by reading a sample of its bytes."""
    with open(file_path, 'rb') as f:
        raw_data = f.read(num_bytes)
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    return encoding

if __name__ == "__main__":
    if not os.path.exists(RAW_CSV_PATH):
        raise FileNotFoundError(f"File not found at {RAW_CSV_PATH}. Please ensure the CSV file is present.")
    
    encoding = detect_file_encoding(RAW_CSV_PATH)
    print(f"Detected encoding for '{RAW_CSV_PATH}': {encoding}")