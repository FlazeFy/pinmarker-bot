import sqlite3

conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()
base_table = 'nlp_history'

# Query
async def get_bot_history(socmed_id:str):
    cursor.execute(f'''
        SELECT command, created_at, COUNT(1) as total 
        FROM {base_table} 
        WHERE socmed_id = ?
        GROUP BY command
    ''', (socmed_id,))
    result = cursor.fetchall()

    if result:
        data_list = [{"command": row[0], "created_at": row[1], "total":row[2]} for row in result]
        return {
            "data": data_list,
            "message": "History found",
            "count": len(data_list)
        }
    else:
        return {
            "data": None,
            "message": "History not found",
            "count": 0
        }
