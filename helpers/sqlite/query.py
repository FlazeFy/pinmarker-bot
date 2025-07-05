import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
DB_SQLITE_PATH = os.getenv("DB_SQLITE_PATH")

def post_user_timezone(socmed_id, socmed_platform, timezone):
    with sqlite3.connect(DB_SQLITE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO user_tz (socmed_id, socmed_platform, timezone)
            VALUES (?, ?, ?)
        ''', (socmed_id, socmed_platform, timezone))
        conn.commit()

def post_ai_command(socmed_id, socmed_platform, command):
    with sqlite3.connect(DB_SQLITE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO nlp_history (socmed_id, socmed_platform, command)
            VALUES (?, ?, ?)
        ''', (socmed_id, socmed_platform, command))
        conn.commit()

def get_user_timezone(socmed_id, socmed_platform):
    with sqlite3.connect(DB_SQLITE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timezone FROM user_tz WHERE socmed_id = ? AND socmed_platform = ?
        ''', (socmed_id, socmed_platform,))
        result = cursor.fetchone()
        return result[0] if result else None