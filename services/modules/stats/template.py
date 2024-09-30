from configs.configs import db
from sqlalchemy import text

async def get_total_item_by_context(tableName, targetColumn, join, userId, where):
    # Query builder
    sql_query = f"""
        SELECT {targetColumn} AS context, COUNT(1) AS total 
        FROM {tableName} 
        {f'JOIN {join}' if join is not None else ''}
        WHERE {tableName}.created_by = '{userId}' 
        {f' AND pin.deleted_at IS NULL ' if tableName in ['pin', 'visit'] else ''}
        {f' AND {where} ' if where is not None else ''}
        GROUP BY {targetColumn}
        ORDER BY total DESC
    """
    compiled_sql = text(sql_query)

    # Exec
    result = db.connect().execute(compiled_sql)
    data = result.fetchall()
    db.connect().close()

    return data