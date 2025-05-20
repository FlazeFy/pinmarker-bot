from services.modules.pin.pin_model import pin
from services.modules.visit.visit_model import visit
from services.modules.user.user_model import user
from configs.configs import db
from sqlalchemy import select, desc, and_, or_
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from sqlalchemy.sql.functions import concat

# Services
from helpers.sqlite.template import get_user_timezone

now = datetime.now()
now_str = now.strftime("%Y-%m-%d%H:%M:%S")

async def get_all_visit_last_day(userId:str, days:str):
    # Query builder
    query = select(
        pin.c.pin_name, 
        concat(pin.c.pin_lat, ',', pin.c.pin_long).label('pin_coordinate'),
        pin.c.pin_category,
        visit.c.visit_desc, 
        visit.c.visit_by, 
        visit.c.visit_with, 
        visit.c.created_at
    ).join(
        pin, pin.c.id == visit.c.pin_id
    ).where(
        visit.c.created_by == userId
    ).order_by(
        desc(visit.c.created_at)
    )

    if days != 'all':
        days_ago = datetime.now() - timedelta(days=int(days))
        query = query.where(visit.c.created_at >= days_ago)

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()

    if data:
        query_user = select(
            user.c.telegram_user_id
        ).where(
            user.c.id == userId
        )
        result_user = db.connect().execute(query_user)
        data_user = result_user.first()
        db.connect().close()

        timezone = get_user_timezone(socmed_id=data_user.telegram_user_id, socmed_platform='telegram')
        timezone_offset = 0
        if timezone:
            timezone_offset = int(timezone[:0] + timezone[0+1:])

        data_list = [dict(row._mapping) for row in data]

        data_list_final = []
        for row in data_list:
            row['created_at'] = (row['created_at'] + timedelta(hours=timezone_offset)).isoformat() 
            data_list_final.append(row)            

        return JSONResponse(
            status_code=200, 
            content={
                "data": data_list_final,
                "message": "Visit history found",
                "count": len(data_list_final),
                "with_timezone": timezone
            }
        )
    else: 
        db.connect().close()
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "Visit history not found",
                "count": 0,
                "with_timezone": None
            }
        )

async def get_all_visit(userId:str):
    # Query builder
    query = select(
        visit.c.id,
        visit.c.visit_desc,
        visit.c.visit_by,
        visit.c.visit_with,
        visit.c.created_at,
        pin.c.pin_name
    ).outerjoin(
        pin, pin.c.id == visit.c.pin_id,
    ).where(
        or_(
            and_(
                pin.c.created_by == userId,
                pin.c.deleted_at.is_(None),
            ),
            visit.c.created_by == userId
        )
    ).order_by(
        visit.c.created_at.desc()
    )

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    data_list = [dict(row._mapping) for row in data]

    if len(data) > 0:
        data_list_final = []
        for row in data:
            data_list = dict(row._mapping)
            data_list['created_at'] = data_list['created_at'].isoformat() 
            data_list_final.append(data_list)
        data_list = data_list_final

        return JSONResponse(
            status_code=200, 
            content={
                "data": data_list,
                "message": "Visit found",
                "count": len(data)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "Visit not found",
                "count": 0
            }
        )
    
async def get_recap_all_weekly_visit():
    # Query Builder
    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    query = select(
        visit.c.visit_desc,
        visit.c.visit_with,
        visit.c.visit_by,
        visit.c.created_at,
        pin.c.pin_name,
        pin.c.pin_category,
        user.c.username,
        user.c.telegram_is_valid,
        user.c.telegram_user_id
    ).outerjoin(
        pin, pin.c.id == visit.c.pin_id,
    ).join(
        user, user.c.id == visit.c.created_by
    ).where(
        pin.c.deleted_at.is_(None),
        visit.c.created_at >= seven_days_ago
    ).order_by(
        user.c.username.asc(),
        visit.c.created_at.asc()
    )

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    if len(data) != 0:
        return data
    else:
        return None
