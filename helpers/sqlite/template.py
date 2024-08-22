import sqlite3

conn = sqlite3.connect('user_data.db')
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

# Command
def post_user_timezone(socmed_id, socmed_platform, timezone):
    cursor.execute('''
        INSERT OR REPLACE INTO user_tz (socmed_id, socmed_platform, timezone)
        VALUES (?, ?, ?)
    ''', (socmed_id, socmed_platform, timezone))
    conn.commit()

def post_ai_command(socmed_id, socmed_platform, command):
    cursor.execute('''
        INSERT OR REPLACE INTO nlp_history (socmed_id, socmed_platform, command)
        VALUES (?, ?, ?)
    ''', (socmed_id, socmed_platform, command))
    conn.commit()

# Query
def get_user_timezone(socmed_id, socmed_platform):
    cursor.execute('''
        SELECT timezone FROM user_tz WHERE socmed_id = ? AND socmed_platform = ?
    ''', (socmed_id, socmed_platform,))
    result = cursor.fetchone()
    return result[0] if result else None
