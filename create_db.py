import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    try:
        # Connect to the default 'postgres' database first
        conn = psycopg2.connect(
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST', '127.0.0.1'),
            port=os.getenv('DB_PORT', '5432'),
            dbname='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'hospital_db'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute('CREATE DATABASE hospital_db')
            print("Successfully created database 'hospital_db'!")
        else:
            print("Database 'hospital_db' already exists.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_database()
