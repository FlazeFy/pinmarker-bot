from services.modules.pin.pin_model import pin
from services.modules.visit.visit_model import visit
from configs.configs import db
import csv
from sqlalchemy import select, desc
import io
from firebase_admin import storage
from datetime import datetime, timedelta

# Services
from helpers.sqlite.template import get_user_timezone

now = datetime.now()
now_str = now.strftime("%Y-%m-%d%H:%M:%S")

async def get_all_visit_last_day(userId:str, teleId:str):
    days = 30
    thirty_days_ago = datetime.now() - timedelta(days=days)

    # Query builder
    query = select(
        pin.c.pin_name, 
        visit.c.visit_desc, 
        visit.c.visit_by, 
        visit.c.visit_with, 
        visit.c.created_at, 
    ).join(
        pin, pin.c.id == visit.c.pin_id
    ).where(
        visit.c.created_by == userId,
        visit.c.created_at >= thirty_days_ago
    ).order_by(
        desc(visit.c.created_at)
    )

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    timezone = get_user_timezone(socmed_id=teleId, socmed_platform='telegram')
    notestz =""

    if timezone:
        notestz = f" based UTC{timezone}"
        timezone_offset = int(timezone[:0] + timezone[0+1:])

    if len(data) != 0:
        res = f"Here is the visit history for last {days}{notestz}:\n"
        day_before = ''

        for dt in data:    
            if isinstance(dt.created_at, str):
                dt_created_at = datetime.strptime(dt.created_at, '%Y-%m-%d %H:%m:%S')
            else:
                dt_created_at = dt.created_at 

            if timezone:
                dt_created_at = dt_created_at + timedelta(hours=timezone_offset)
            
            if day_before == '' or day_before != dt_created_at.strftime('%d %b %Y'):
                day_before = dt_created_at.strftime('%d %b %Y')
                res += f"\n<b>{day_before}</b>\n"
                date = dt_created_at.strftime('%H:%M')
            else: 
                date = dt_created_at.strftime('%H:%M')
                        
            res += f"- Visit at {dt.pin_name} using {dt.visit_by} {'with '+dt.visit_with+' ' if dt.visit_with else ''}at {date}\n"

        return res
    else:
        return '<i>- No visit found -</i>'

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
            