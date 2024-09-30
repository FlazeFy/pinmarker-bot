from configs.configs import db
from sqlalchemy import text
from sqlalchemy import select, desc, and_
from datetime import datetime
from fastapi.responses import JSONResponse

from services.modules.pin.pin_model import pin
from services.modules.visit.visit_model import visit
from services.modules.stats.template import get_total_item_by_context

async def get_stats(userId:str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    userId = "fcd3f23e-e5aa-11ee-892a-3216422910e9"

    dt_total_pin_by_category = await get_total_item_by_context(tableName="pin", join=None, targetColumn="pin_category", userId=userId, where=None)
    dt_total_visit_by_category = await get_total_item_by_context(tableName="visit", join="pin on pin.id = visit.pin_id", targetColumn="pin_category", userId=userId, where=None)
    dt_total_gallery_by_pin = await get_total_item_by_context(tableName="gallery", join="pin on pin.id = gallery.pin_id", targetColumn="pin_name", userId=userId, where=None)

    year = datetime(datetime.now().year, 1, 1).strftime('%Y')
    sql_visit_by_month = text(f"""
        SELECT DATE_FORMAT(visit.created_at, '%M') AS context, COUNT(1) AS total
        FROM visit
        JOIN pin ON visit.pin_id = pin.id
        WHERE pin.deleted_at IS NULL
        AND pin.created_by = '{userId}'
        AND YEAR(visit.created_at) = '{year}'
        GROUP BY context
        ORDER BY context DESC
    """)
    result = db.connect().execute(sql_visit_by_month)
    data_visit_by_month = [dict(zip(result.keys(), row)) for row in result.fetchall()]
    dt_total_visit_by_month = []
    db.connect().close()

    for m in months:
        for dt in data_visit_by_month:
            if m == dt['context']:
                dt_total_visit_by_month.append({
                    'context': dt['context'],
                    'total': dt['total']
                })
        dt_total_visit_by_month.append({
            'context': m,
            'total': 0
        })
            

    res = f"<b>Total Pin By Category:</b>\n"
    for dt in dt_total_pin_by_category:
        res += f"- {dt.context} : {dt.total}\n"

    res += f"\n<b>Total Visit By Category:</b>\n"
    for dt in dt_total_visit_by_category:
        res += f"- {dt.context} : {dt.total}\n"

    res += f"\n<b>Total Gallery By Pin:</b>\n"
    for dt in dt_total_gallery_by_pin:
        res += f"- {dt.context} : {dt.total}\n"

    res += f"\n<b>Total Visit By Month in {year}:</b>\n"
    for dt in dt_total_visit_by_month:
        res += f"- {dt['context']} : {dt['total']}\n"

    return res

async def get_dashboard(userId:str, role:str):
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
    result_total_marker = db.connect().execute(compiled_sql_total_marker)
    data_total_marker = result_total_marker.first()

    result_total_favorite = db.connect().execute(compiled_sql_total_favorite)
    data_total_favorite = result_total_favorite.first()

    result_most_category = db.connect().execute(compiled_sql_most_category)
    data_most_category = result_most_category.first()

    result_last_added = db.connect().execute(query_last_added)
    data_last_added = result_last_added.first()

    result_most_visit = db.connect().execute(compiled_sql_most_visit)
    data_most_visit = result_most_visit.first()

    result_last_visit = db.connect().execute(query_last_visit)
    data_last_visit = result_last_visit.first()
    db.connect().close()

    data = {
        'total_marker': data_total_marker.total,
        'total_favorite': data_total_favorite.total,
        'most_category': f"({data_most_category.total if data_most_category else '-'}) {data_most_category.context if data_most_category else '-'}",
        'last_added': data_last_added.pin_name if data_last_added else '-',
    }
    
    if role == 'user':
        data.update({
            'last_visit': data_last_visit.pin_name if data_last_visit else '-',
            'most_visit': f"({data_most_visit.total if data_most_visit else '-'}) {data_most_visit.context if data_most_visit else '-'}",
        })

    return JSONResponse(
        status_code=200, 
        content={
            "data": data,
            "message": "Dashboard found",
        }
    )