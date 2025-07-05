import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
DB_SQLITE_PATH = os.getenv("DB_SQLITE_PATH")

def init_db_sqlite():
    with sqlite3.connect(DB_SQLITE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_tz (
                socmed_id TEXT PRIMARY KEY, 
                socmed_platform TEXT(14),
                timezone TEXT(6),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nlp_history (
                socmed_id TEXT PRIMARY KEY, 
                socmed_platform TEXT(14),
                command TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()

