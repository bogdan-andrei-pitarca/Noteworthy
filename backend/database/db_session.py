import psycopg
import logging
import os
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
logging.basicConfig(level=logging.INFO)

def get_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    if not DB_PASSWORD:
        logging.error("FATAL: DB_PASSWORD environment variable is not set. Please update .env file.")
        raise ValueError("Database password is required to establish connection.")
    try:
        conn = psycopg.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        logging.info("Database connection established.")
        return conn
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        raise

def initialize_database(conn):
    """Initializes the database by creating necessary tables."""
    sql_schema = """
    CREATE TABLE IF NOT EXISTS fragrances (
            -- Primary Key and Foreign Key to FAISS index
            embedding_id INT PRIMARY KEY, 
            -- Structured Fragrance Data
            perfume_name VARCHAR(255) NOT NULL,
            brand VARCHAR(255),
            gender VARCHAR(50),
            launch_year INT,
            rating_value DECIMAL(3, 2),
            rating_count INT,        -- useful for filtering/sorting by popularity
            url TEXT,               
            -- Main Accords (useful for filtering/searching)
            main_accord_1 VARCHAR(50),
            main_accord_2 VARCHAR(50),
            main_accord_3 VARCHAR(50),
            main_accord_4 VARCHAR(50),
            main_accord_5 VARCHAR(50),
            -- Text data used for AI/Display
            all_notes TEXT,        
            embedding_text TEXT    
        );
    """

    try:
        with conn.cursor() as cur:
            cur.execute(sql_schema)
            conn.commit()
            logging.info("Database initialized and tables created (if not exist).")
    except Exception as e:
        logging.error(f"Error initializing the database: {e}")
        raise

if __name__ == "__main__":
    try:
        conn = get_connection()
        initialize_database(conn)
        conn.close()
        logging.info("Database setup complete.")
    except Exception as e:
        logging.error(f"Database setup failed: {e}")