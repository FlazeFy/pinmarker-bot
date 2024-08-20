import sqlite3

conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_tz (
        telegram_id INTEGER PRIMARY KEY,
        timezone TEXT
    )
''')

conn.commit()

def post_user_timezone(telegram_id, timezone):
    cursor.execute('''
        INSERT OR REPLACE INTO user_tz (telegram_id, timezone)
        VALUES (?, ?)
    ''', (telegram_id, timezone))
    conn.commit()

def get_user_timezone(telegram_id):
    cursor.execute('''
        SELECT timezone FROM user_tz WHERE telegram_id = ?
    ''', (telegram_id,))
    result = cursor.fetchone()
    return result[0] if result else None
