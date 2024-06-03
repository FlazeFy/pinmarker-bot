from configs.configs import con
from sqlalchemy import text
from sqlalchemy import select, desc, and_

from services.modules.pin.pin_model import pin
from services.modules.visit.visit_model import visit

async def get_dashboard():
    userId = "fcd3f23e-e5aa-11ee-892a-3216422910e9"

    # Query builder
    sql_total_marker = f"""
        SELECT COUNT(1) AS total
        FROM pin
        WHERE created_by = '{userId}'
    """
    compiled_sql_total_marker = text(sql_total_marker)

    sql_total_favorite = f"""
        SELECT COUNT(1) AS total
        FROM pin
        WHERE created_by = '{userId}'
        AND is_favorite = 1
    """
    compiled_sql_total_favorite = text(sql_total_favorite)

    query_last_visit = select(
        pin.c.pin_name
    ).join(
        visit, visit.c.pin_id == pin.c.id
    ).where(
        and_(
            visit.c.created_by == userId,
            pin.c.deleted_at.is_(None) 
        )
    ).order_by(
        desc(visit.c.created_at)
    )

    sql_most_visit = f"""
        SELECT pin_name as context, COUNT(1) as total
        FROM pin
        JOIN visit ON visit.pin_id = pin.id
        WHERE visit.created_by = '{userId}'
        GROUP BY pin_name
    """
    compiled_sql_most_visit = text(sql_most_visit)

    sql_most_category = f"""
        SELECT pin_category as context, COUNT(1) as total
        FROM pin
        WHERE created_by = '{userId}'
        GROUP BY context
        ORDER BY total DESC
    """
    compiled_sql_most_category = text(sql_most_category)

    query_last_added = select(
        pin.c.pin_name
    ).where(
        and_(
            pin.c.created_by == userId,
            pin.c.deleted_at.is_(None) 
        )
    ).order_by(
        desc(pin.c.created_at)
    )

    # Exec
    result_total_marker = con.execute(compiled_sql_total_marker)
    data_total_marker = result_total_marker.first()

    result_total_favorite = con.execute(compiled_sql_total_favorite)
    data_total_favorite = result_total_favorite.first()

    result_most_visit = con.execute(compiled_sql_most_visit)
    data_most_visit = result_most_visit.first()

    result_most_category = con.execute(compiled_sql_most_category)
    data_most_category = result_most_category.first()

    result_last_visit = con.execute(query_last_visit)
    data_last_visit = result_last_visit.first()

    result_last_added = con.execute(query_last_added)
    data_last_added = result_last_added.first()
    
    res = (
        f"<b>Total Marker: {data_total_marker.total}</b>\n"
        f"<b>Total Favorite : {data_total_favorite.total}</b>\n"
        f"<b>Last Visit : {data_last_visit.pin_name}</b>\n"
        f"<b>Most Visit : ({data_most_visit.total}) {data_most_category.context}</b>\n"
        f"<b>Most Category : ({data_most_category.total}) {data_most_category.context}</b>\n"
        f"<b>Last Added : {data_last_added.pin_name}</b>\n"
    )

    return res