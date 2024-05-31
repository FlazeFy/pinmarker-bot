from services.modules.pin.pin_model import pin
from services.modules.visit.visit_model import visit
from configs.configs import con
from sqlalchemy import select, and_
from sqlalchemy.sql.functions import concat

async def get_all_pin():
    # Query builder
    query = select(
        pin.c.pin_name,
        pin.c.pin_desc,
        concat(pin.c.pin_lat, ',', pin.c.pin_long).label('pin_coordinate'),
        pin.c.pin_category,
        pin.c.pin_person
    ).where(
        pin.c.created_by == "fcd3f23e-e5aa-11ee-892a-3216422910e9",
    ).order_by(
        pin.c.pin_category.asc(),
        pin.c.pin_name.asc()
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    res = f"You have {len(data)} pins.\nHere is the list:\n"
    pin_category_before = ''
    i = 1

    for dt in data:
        if pin_category_before == '' or pin_category_before != dt.pin_category:
            res += f"<b>Category: {dt.pin_category}</b>\n"
            pin_category_before = dt.pin_category
            i = 1
        
        res += (
            f"<b>{i}. {dt.pin_name}</b>\n"
            f"Notes : {dt.pin_desc or '<i>- No Description Provided -</i>'}\n"
            f"Person In Contact : {dt.pin_person or '-'}\n"
            f"https://www.google.com/maps/place/{dt.pin_coordinate}\n\n"
        )
        i += 1

    return res

async def get_all_pin_name():
    # Query builder
    query = select(
        pin.c.id,
        pin.c.pin_name,
    ).where(
        pin.c.created_by == "fcd3f23e-e5aa-11ee-892a-3216422910e9",
    ).order_by(
        pin.c.pin_name.asc()
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    return data

async def get_detail_pin(id):
    # Query builder
    query_pin = select(
        pin.c.pin_name,
        pin.c.pin_desc,
        pin.c.pin_lat,
        pin.c.pin_long,
        pin.c.pin_category,
        pin.c.pin_person,
        pin.c.pin_call,
        pin.c.pin_email,
        pin.c.pin_address,
        pin.c.is_favorite,
        pin.c.created_at,
        pin.c.updated_at
    ).where(
        and_(
            pin.c.created_by == "fcd3f23e-e5aa-11ee-892a-3216422910e9",
            pin.c.id == id
        )
    )

    query_visit = select(
        visit.c.visit_desc,
        visit.c.visit_by,
        visit.c.visit_with,
        visit.c.created_at
    ).where(
        and_(
            visit.c.created_by == "fcd3f23e-e5aa-11ee-892a-3216422910e9",
            visit.c.pin_id == id
        )
    )

    # Exec
    result_pin = con.execute(query_pin)
    data_pin = result_pin.first()

    result_visit = con.execute(query_visit)
    data_visit = result_visit.fetchall()

    res = (
        f"<b>{data_pin.pin_name}</b>\n"
        f"Latitude : {data_pin.pin_lat}\n"
        f"Longitude : {data_pin.pin_long}\n"
        f"Person In Touch : {data_pin.pin_person or '-'}\n"
        f"Email : {data_pin.pin_email or '-'}\n"
        f"Phone Number : {data_pin.pin_call or '-'}\n"
        f"Address : {data_pin.pin_address or '-'}\n"
        f"Description : {data_pin.pin_desc or '-'}\n\n"
        f"{'' if data_pin.is_favorite != 1 else 'This pin is favorited!'}\n\n"
        f"<b>Props</b>\n"
        f"Created At : {data_pin.created_at}\n"
        f"Updated At : {data_pin.updated_at or '-'}\n\n"
        f"<b>Visit History</b>\n"
    )

    if data_visit:
        for index, dt in enumerate(data_visit, start=1):
            date = dt.created_at.strftime('%d %b %Y %H:%M')
            res += f"{index}. {dt.visit_desc} using {dt.visit_by} {'with '+dt.visit_with+' ' if dt.visit_with else ''}at {date}\n"
    else:
        res += '<i>- This location has never been visited -</i>'

    return res, data_pin.pin_lat, data_pin.pin_long