from services.modules.pin.pin_model import pin
from services.modules.visit.visit_model import visit
from services.modules.user.user_model import user
from configs.configs import db
import csv
from sqlalchemy import select, desc, and_, or_
import io
from firebase_admin import storage
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse

# Services
from helpers.sqlite.template import get_user_timezone

now = datetime.now()
now_str = now.strftime("%Y-%m-%d%H:%M:%S")

async def get_all_visit_last_day(userId:str, days:str):
    # Query builder
    query = select(
        pin.c.pin_name, 
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

async def get_all_visit_csv(platform:str, userId:str, teleId:str):
    # Query builder
    query = select(
        pin.c.pin_name, 
        pin.c.pin_category, 
        pin.c.pin_lat, 
        pin.c.pin_long, 
        pin.c.pin_address, 
        visit.c.visit_desc, 
        visit.c.visit_by, 
        visit.c.visit_with, 
        visit.c.created_at.label('visit_created_at'), 
        pin.c.created_at.label('pin_created_at')
    ).join(
        pin, pin.c.id == visit.c.pin_id
    ).where(
        visit.c.created_by == userId
    ).order_by(
        desc(visit.c.created_at)
    )

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    if len(data) != 0:
        output = io.StringIO()
        writer = csv.writer(output)

        timezone = get_user_timezone(socmed_id=teleId, socmed_platform='telegram')
        notestz = "(GMT)"

        if timezone:
            timezone_offset = int(timezone[:0] + timezone[0+1:])
            notestz = f"(UTC{timezone})"

        # Header
        writer.writerow([
            "Pin Name", 
            "Pin Category", 
            "Pin Coordinate", 
            "Visit Context", 
            "Pin Address", 
            f"Visit Created At {notestz}", 
            f"Pin Created At {notestz}"
        ])

        for dt in data:
            if dt.visit_created_at == '0000-00-00 00:00:00':
                visit_created_at = '-'
            elif isinstance(dt.visit_created_at, str):
                visit_created_at = datetime.strptime(dt.visit_created_at, '%Y-%m-%d %H:%m:%S')
            else:
                visit_created_at = dt.visit_created_at 

            if dt.pin_created_at == '0000-00-00 00:00:00':
                pin_created_at = '-' 
            elif isinstance(dt.pin_created_at, str):
                pin_created_at = datetime.strptime(dt.pin_created_at, '%Y-%m-%d %H:%m:%S')
            else:
                pin_created_at = dt.pin_created_at  

            if visit_created_at != '-' and timezone:
                visit_created_at = visit_created_at + timedelta(hours=timezone_offset)
            
            if timezone:
                pin_created_at = pin_created_at + timedelta(hours=timezone_offset)

            writer.writerow([
                dt.pin_name, 
                dt.pin_category, 
                f"{dt.pin_lat}, {dt.pin_long}", 
                f"{dt.visit_desc+' ' if dt.visit_desc else ''}using {dt.visit_by} {'with '+dt.visit_with+' ' if dt.visit_with else ''}", 
                dt.pin_address if dt.pin_address else '-', 
                visit_created_at, 
                pin_created_at
            ])

        csv_content = output.getvalue()    
        output.seek(0)
        
        # Firebase Storage
        bucket = storage.bucket()
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        fileName = f"visit_history_{userId}_{now_str}.csv"
        blob = bucket.blob(f"generated_data/visit/{fileName}")
        blob.upload_from_string(csv_content, content_type="text/csv")
        
        if platform == 'telegram':
            return csv_content, fileName
        elif platform == 'discord':
            return output, fileName
    else:
        return None, 'No data to export'

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