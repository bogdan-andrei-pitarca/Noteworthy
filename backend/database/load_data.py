import pandas as pd
import psycopg
import logging
import os
from database.db_session import get_connection, initialize_database

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'fra_data_processed.csv')

logging.basicConfig(level=logging.INFO)

def load_data_to_db():
    try:
        conn = get_connection()
        initialize_database(conn)
        
        df = pd.read_csv(DATA_PATH, encoding='latin1')
        logging.info(f"Loaded data from {DATA_PATH} with {len(df)} records.")
        
        records_to_insert = []
        for index, row in df.iterrows():
            rating_value_str = str(row['Rating Value']).replace(',', '.')
            rating_value_float = float(rating_value_str) if pd.notna(rating_value_str) else None

            year_of_release = int(row['Year']) if pd.notna(row['Year']) else None

            rating_count = int(row['Rating Count']) if pd.notna(row['Rating Count']) else None

            all_notes_str = str(row['all_notes'])

            records_to_insert.append(( 
                int(row['embedding_id']),
                row['url'],
                row['Perfume'],
                row['Brand'],
                row['Gender'],
                year_of_release,
                rating_value_float,
                rating_count,
                row['mainaccord1'],
                row['mainaccord2'],
                row['mainaccord3'],
                row['mainaccord4'],
                row['mainaccord5'],
                all_notes_str,
                row['embedding_text']
            ))

            # insert using batch insertion
        with conn.cursor() as cur:
            insert_query = """
            INSERT INTO fragrances (
                embedding_id, url, perfume_name, brand, gender,
                launch_year, rating_value, rating_count,
                main_accord_1, main_accord_2, main_accord_3, main_accord_4, main_accord_5,
                all_notes, embedding_text
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (embedding_id) DO NOTHING;
            """

            cur.executemany(insert_query, records_to_insert)
            conn.commit()
        
        logging.info(f"Inserted {len(records_to_insert)} records into the database.")
    
    except Exception as e:
        logging.error(f"Error loading data into the database: {e}")
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    load_data_to_db()