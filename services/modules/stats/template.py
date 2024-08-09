from configs.configs import con
from sqlalchemy import text

async def get_total_item_by_context(tableName, targetColumn, join, userId):
    # Query builder
    sql_query = f"""
        SELECT {targetColumn} AS context, COUNT(1) AS total 
        FROM {tableName} 
        {f'JOIN {join}' if join is not None else ''}
        WHERE {tableName}.created_by = '{userId}' 
        {f'AND pin.deleted_at IS NULL' if tableName in ['pin', 'visit'] else ''}
        GROUP BY {targetColumn}
        ORDER BY total DESC
    """
    compiled_sql = text(sql_query)

    # Exec
    result = con.execute(compiled_sql)
    data = result.fetchall()

    return data