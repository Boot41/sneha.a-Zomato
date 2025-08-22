
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

# Load environment variables from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "zomato_clone")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres123")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_db():
    """
    Get a new database connection.
    Remember to close() after use.
    """
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        cursor_factory=RealDictCursor
    )
    return conn
