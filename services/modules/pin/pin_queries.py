from services.modules.pin.pin_model import pin
from configs.configs import con
from sqlalchemy import select
from sqlalchemy.sql.functions import concat

async def get_all_pin():
    # Query builder
    query = select(
        pin.c.pin_name,
        pin.c.pin_desc,
        concat(pin.c.pin_lat, ',', pin.c.pin_long).label('pin_coordinate'),
        pin.c.pin_category,
        pin.c.pin_person
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
            f"Notes : {dt.pin_desc}\n"
            f"Person In Contact : {dt.pin_person}\n"
            f"https://www.google.com/maps/place/{dt.pin_coordinate}\n\n"
        )
        i += 1

    return res