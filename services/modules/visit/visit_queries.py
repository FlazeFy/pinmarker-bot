from services.modules.pin.pin_model import pin
from services.modules.visit.visit_model import visit
from configs.configs import con
from sqlalchemy import select, desc, and_

async def get_all_visit():
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
        visit.c.created_by == "fcd3f23e-e5aa-11ee-892a-3216422910e9"
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

