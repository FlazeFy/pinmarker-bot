from services.modules.pin.pin_model import pin
from services.modules.visit.visit_model import visit
from configs.configs import con
from sqlalchemy import select, and_
from sqlalchemy.sql.functions import concat
from helpers.converter import calculate_distance

async def get_all_pin(type:str, userId:str):
    # Query builder
    query = select(
        pin.c.pin_name,
        pin.c.pin_desc,
        concat(pin.c.pin_lat, ',', pin.c.pin_long).label('pin_coordinate'),
        pin.c.pin_category,
        pin.c.pin_person
    ).where(
        pin.c.created_by == userId,
    ).order_by(
        pin.c.pin_category.asc(),
        pin.c.pin_name.asc()
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    res = f"You have {len(data)} pins.\nHere is the list:\n"
    pin_category_before = ''

    if type == 'bot':
        for idx, dt in enumerate(data, start=1):
            if pin_category_before == '' or pin_category_before != dt.pin_category:
                res += f"<b>Category: {dt.pin_category}</b>\n\n"
                pin_category_before = dt.pin_category
            
            res += (
                f"<b>{idx}. {dt.pin_name}</b>\n"
                f"Notes : {dt.pin_desc or '<i>- No Description Provided -</i>'}\n"
                f"Person In Contact : {dt.pin_person or '-'}\n"
                f"https://www.google.com/maps/place/{dt.pin_coordinate}\n\n"
            )

        return res
    elif type == 'api':
        data_list = [dict(row._mapping) for row in data]
        return {
            "data": data_list,
            "message": "Pin found",
            "count": len(data)
        }
    
async def get_pin_by_name(name:str):
    # Query builder
    query = select(
        pin.c.pin_name,
        pin.c.pin_lat,
        pin.c.pin_long,
        pin.c.pin_category
    ).where(
        and_(
            pin.c.created_by == "fcd3f23e-e5aa-11ee-892a-3216422910e9",
            pin.c.pin_name.ilike(f'%{name}%'),
        )
    ).order_by(
        pin.c.pin_name.asc()
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    data_list = [dict(row._mapping) for row in data]

    if len(data) > 0:
        return {
            "data": data_list,
            "message": "Pin found",
            "count": len(data)
        }
    else:
        return {
            "data": None,
            "message": "Pin not found",
        }

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

async def get_pin_distance_by_coor(coor:str):
    # Query builder
    query = select(
        pin.c.pin_name,
        pin.c.pin_lat,
        pin.c.pin_long,
        pin.c.pin_person,
        pin.c.pin_call,
        pin.c.pin_email,
        pin.c.pin_address
    ).where(
        pin.c.created_by == "fcd3f23e-e5aa-11ee-892a-3216422910e9",
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()
    res = ''

    if data:
        pin_data = []
        
        for dt in data:
            distance = calculate_distance(coor, f"{dt.pin_lat},{dt.pin_long}")
            pin_data.append({
                'pin_name': dt.pin_name,
                'pin_lat': dt.pin_lat,
                'pin_long': dt.pin_long,
                'pin_person': dt.pin_person,
                'pin_call': dt.pin_call,
                'pin_email': dt.pin_email,
                'pin_address': dt.pin_address,
                'distance': distance
            })

        # Order by distance
        pin_data.sort(key=lambda x: x['distance'])

        res += f"<b>Showing pin by closest distance :</b>\n\n"
        for dt in pin_data:
            distance = dt['distance']
            if distance > 1000:
                distance = distance / 1000
                distance = f"{distance:.2f} km"
            else:
                distance = f"{distance:.2f} m"

            res += (
                f"<b>{dt['pin_name']}</b>\n"
                f"Distance from Me: <b>{distance}</b>\n\n"
                f"<b>Contact</b>\n"
                f"Person in Touch : {dt['pin_person'] or '-'}\n"
                f"Phone Number : {dt['pin_call'] or '-'}\n"
                f"Email : {dt['pin_email'] or '-'}\n"
                f"Address : {dt['pin_address'] or '-'}\n\n"
                f"========== || ========== || ==========\n\n"
            )
    else:
        res += '<i>- You have no location saved -</i>'

    return res

async def get_find_all(search:str, type:str):
    res = ''

    if type == 'ai':
        # Query builder
        query_cat = select(
            pin.c.pin_name,
            concat(pin.c.pin_lat, ',', pin.c.pin_long).label('pin_coordinate')
        ).where(
            and_(
                pin.c.created_by == "fcd3f23e-e5aa-11ee-892a-3216422910e9",
                pin.c.pin_category == search
            )
        )

        query_pin = select(
            pin.c.pin_name,
            concat(pin.c.pin_lat, ',', pin.c.pin_long).label('pin_coordinate')
        ).where(
            and_(
                pin.c.created_by == "fcd3f23e-e5aa-11ee-892a-3216422910e9",
                pin.c.pin_name.ilike(f'%{search}%')
            )
        )

        query_person = select(
            pin.c.pin_name,
            pin.c.pin_person,
            concat(pin.c.pin_lat, ',', pin.c.pin_long).label('pin_coordinate')
        ).where(
            and_(
                pin.c.created_by == "fcd3f23e-e5aa-11ee-892a-3216422910e9",
                pin.c.pin_person.ilike(f'%{search}%')
            )
        ).order_by(
            pin.c.pin_name.asc()
        )

        # Exec
        result_cat = con.execute(query_cat)
        result_pin = con.execute(query_pin)
        result_person = con.execute(query_person)
        data_cat = result_cat.fetchall()
        data_pin = result_pin.fetchall()
        data_person = result_person.fetchall()

        if data_cat or data_pin:
            if data_cat:
                res += f'Based on category <b>{search}</b>, I found {len(data_cat)} marker:\n\n'
                for idx, dt in enumerate(data_cat, start=1):            
                    res += (
                        f"<b>{idx}. {dt.pin_name}</b>\n"
                        f"https://www.google.com/maps/place/{dt.pin_coordinate}\n\n"
                    )
            else:
                res += "I don't find any category\n\n"
            
            if data_pin:
                res += f'Based on pin name <b>{search}</b>, I found {len(data_pin)} marker:\n\n'
                for idx, dt in enumerate(data_pin, start=1):            
                    res += (
                        f"<b>{idx}. {dt.pin_name}</b>\n"
                        f"https://www.google.com/maps/place/{dt.pin_coordinate}\n\n"
                    )
            else:
                res += "I don't find any pin"

            if data_person:
                res += f'Based on person in touch <b>{search}</b>, I found {len(data_pin)} marker:\n\n'
                for idx, dt in enumerate(data_person, start=1):            
                    res += (
                        f"<b>{idx}. {dt.pin_name} - {dt.pin_person}</b>\n"
                        f"https://www.google.com/maps/place/{dt.pin_coordinate}\n\n"
                    )
            else:
                res += "I don't find any person"
        else:
            res += f'No data found for both category and pin name based on {search}\n'

    return res

# External Apps
async def get_pin_by_category_query(category:str,user_id:str):
    list_category = category.split(',')

    # Query builder
    query = select(
        pin.c.pin_name,
        pin.c.pin_desc,
        pin.c.pin_lat,
        pin.c.pin_long,
        pin.c.pin_person,
        pin.c.pin_address,
        pin.c.pin_call,
        pin.c.pin_email
    ).where(
        and_(
            pin.c.created_by == user_id,
            pin.c.pin_category.in_(list_category)
        )
    ).order_by(
        pin.c.pin_name.asc()
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    data_list = [dict(row._mapping) for row in data]

    if len(data) > 0:
        return {
            "data": data_list,
            "message": "Pin found",
            "count": len(data)
        }
    else:
        return {
            "data": None,
            "message": "Pin not found",
        }