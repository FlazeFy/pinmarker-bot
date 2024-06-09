from services.modules.pin.pin_model import pin
from services.modules.visit.visit_model import visit
from configs.configs import con
import csv
from sqlalchemy import select, desc
import firebase_admin
import io
from firebase_admin import credentials, storage
from datetime import datetime

cred = credentials.Certificate("configs/pinmarker-36552-firebase-adminsdk-5dett-b688b092f1.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'pinmarker-36552.appspot.com'
})
now = datetime.now()
now_str = now.strftime("%Y-%m-%d%H:%M:%S")

async def get_all_visit():
    userId = "fcd3f23e-e5aa-11ee-892a-3216422910e9"

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
        visit.c.created_by == userId
    ).order_by(
        desc(visit.c.created_at)
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    res = f"Here is the visit history:\n"
    day_before = ''

    for dt in data:    
        if day_before == '' or day_before != dt.created_at.strftime('%d %b %Y'):
            day_before = dt.created_at.strftime('%d %b %Y')
            res += f"\n<b>"+day_before+"</b>\n"
            date = dt.created_at.strftime('%H:%M')
        else: 
            date = dt.created_at.strftime('%H:%M')
                
        res += f"- Visit at {dt.pin_name} using {dt.visit_by} {'with '+dt.visit_with+' ' if dt.visit_with else ''}at {date}\n"
    return res

async def get_all_visit_csv(platform:str):
    userId = "fcd3f23e-e5aa-11ee-892a-3216422910e9"

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
    result = con.execute(query)
    data = result.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "Pin Name", 
        "Pin Category", 
        "Pin Coordinate", 
        "Visit Context", 
        "Pin Address", 
        "Visit Created At", 
        "Pin Created At"
    ])

    for dt in data:
        writer.writerow([
            dt.pin_name, 
            dt.pin_category, 
            f"{dt.pin_lat}, {dt.pin_long}", 
            f"{dt.visit_desc+' ' if dt.visit_desc else ''}using {dt.visit_by} {'with '+dt.visit_with+' ' if dt.visit_with else ''}", 
            dt.pin_address if dt.pin_address else '-', 
            dt.visit_created_at.strftime("%Y-%m-%d %H:%M:%S"), 
            dt.pin_created_at.strftime("%Y-%m-%d %H:%M:%S")
        ])

    csv_content = output.getvalue()    
    output.seek(0)
    
    # Firebase Storage
    bucket = storage.bucket()
    fileName = f"visit_history_{userId}_{now_str}.csv"
    blob = bucket.blob(f"generated_data/visit/{fileName}")
    blob.upload_from_string(csv_content, content_type="text/csv")
    
    if platform == 'telegram':
        return csv_content, fileName
    elif platform == 'discord':
        return output, fileName


