import psycopg
import logging
from typing import List, Optional, Dict 
from database.db_session import get_connection

logging.basicConfig(level=logging.INFO)

def get_fragrances_by_ids(embedding_ids: List[int]) -> List[Dict]:
    """Fetch fragrance details from the database given a list of embedding IDs.
    Args:
        embedding_ids (List[int]): List of embedding IDs to fetch.
    Returns:
        List[Dict]: List of dictionaries containing fragrance details.
    """
    if not embedding_ids:
        logging.info("No embedding IDs provided.")
        return []

    placeholders = ','.join(['%s'] * len(embedding_ids))

    sql_query = f"""
        SELECT 
            embedding_id, perfume_name, brand, gender, launch_year, 
            rating_value, rating_count, url, 
            main_accord_1, main_accord_2, main_accord_3, main_accord_4, main_accord_5,
            all_notes 
        FROM fragrances
        WHERE embedding_id IN ({placeholders});
    """
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(sql_query, embedding_ids)
  
            columns = [desc[0] for desc in cur.description]
            fragrances = [
                dict(zip(columns, row)) for row in cur.fetchall()
            ]
            logging.info(f"Fetched {len(fragrances)} fragrances from the database.")
            return fragrances
    except Exception as e:
        logging.error(f"Error fetching fragrances: {e}")
        return []
    finally:
        if conn:
            conn.close()