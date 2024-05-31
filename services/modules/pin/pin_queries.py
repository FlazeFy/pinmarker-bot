from services.modules.pin.pin_model import pin
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
            res += f"Category: {dt.pin_category}\n"
            pin_category_before = dt.pin_category
            i = 1
        
        res += (
            f"{i}. {dt.pin_name}\n"
            f"Notes : {dt.pin_desc or '- No Description Provided -'}\n"
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
    query = select(
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

    # Exec
    result = con.execute(query)
    data = result.first()

    res = (
        f"{data.pin_name}\n"
        f"Latitude : {data.pin_lat}\n"
        f"Longitude : {data.pin_long}\n"
        f"Person In Touch : {data.pin_person or '-'}\n"
        f"Email : {data.pin_email or '-'}\n"
        f"Phone Number : {data.pin_call or '-'}\n"
        f"Address : {data.pin_address or '-'}\n"
        f"Description : {data.pin_desc or '-'}\n\n"
        f"{'' if data.is_favorite != 1 else 'This pin is favorited!'}\n\n"
        f"Props\n"
        f"Created At : {data.created_at}\n"
        f"Updated At : {data.updated_at or '-'}\n"
    )

    return res, data.pin_lat, data.pin_long