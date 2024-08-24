from services.modules.pin.pin_model import pin
from services.modules.pin.global_list_model import global_list
from services.modules.pin.global_list_rel_model import global_list_pin_relation
from services.modules.user.user_model import user
from services.modules.visit.visit_model import visit
from configs.configs import con
from sqlalchemy import select, and_, func, or_, case
from sqlalchemy.sql.functions import concat
from helpers.converter import calculate_distance

async def get_all_pin(userId:str, platform:str):
    # Query builder
    if platform == 'telegram':
        query = select(
            pin.c.pin_name,
            pin.c.pin_desc,
            concat(pin.c.pin_lat, ',', pin.c.pin_long).label('pin_coordinate'),
            pin.c.pin_category,
            pin.c.pin_person,
            pin.c.pin_address,
            pin.c.created_at
        ).where(
            pin.c.created_by == userId,
        ).order_by(
            pin.c.pin_category.asc(),
            pin.c.pin_name.asc()
        )
    else:
        query = select(
            pin.c.pin_name,
            pin.c.pin_desc,
            case(
                (global_list_pin_relation.c.pin_id.is_not(None), concat(pin.c.pin_lat, ',', pin.c.pin_long)), 
                else_='- hidden -').label('pin_coordinate'),
            pin.c.pin_category,
            pin.c.pin_person,
            case(
                (global_list_pin_relation.c.pin_id.is_not(None), pin.c.pin_address), 
                else_='- hidden -').label('pin_address'),
            pin.c.pin_call,
            pin.c.pin_email,
            pin.c.created_at,
            user.c.username.label('created_by'),
            case(
                (global_list_pin_relation.c.pin_id.is_not(None), True), 
                else_=False).label('is_global_shared'),
        ).join(
            user, user.c.id == pin.c.created_by
        ).outerjoin(
            global_list_pin_relation, global_list_pin_relation.c.pin_id == pin.c.id
        ).where(
            pin.c.deleted_at.is_(None)
        ).order_by(
            pin.c.pin_category.asc(),
            pin.c.pin_name.asc()
        ).group_by(
            pin.c.id
        )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    if len(data) != 0:
        data_list = [dict(row._mapping) for row in data]
        return {
            "data": data_list,
            "message": "Pin found",
            "count": len(data)
        }
    else:
        return {
            "data": None,
            "message": "Pin not found",
            "count": 0
        }
    
async def get_all_pin_export_query(userId:str, platform:str):
    # Query builder
    if platform == 'telegram':
        query = select(
            pin.c.pin_name,
            pin.c.pin_lat,
            pin.c.pin_long,
        ).where(
            and_(
                pin.c.created_by == userId,
                pin.c.deleted_at.is_(None)
            )
        ).order_by(
            pin.c.pin_name.asc()
        )
    else:
        query = select(
            pin.c.pin_name,
            pin.c.pin_lat,
            pin.c.pin_long,
            pin.c.created_at,
            user.c.username.label('created_by')
        ).join(
            user, user.c.id == pin.c.created_by
        ).where(
            pin.c.deleted_at.is_(None)
        ).order_by(
            pin.c.pin_name.asc()
        )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    if len(data) != 0:
        data_list = [dict(row._mapping) for row in data]
        return {
            "data": data_list,
            "message": "Pin found",
            "count": len(data)
        }
    else:
        return {
            "data": None,
            "message": "Pin not found",
            "count": 0
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
            "count": 0
        }
    
async def get_global_list_query(search:str):
    # Query builder
    query = select(
        global_list.c.id,
        func.coalesce(
            func.group_concat(
                func.coalesce(pin.c.pin_name, None),
            ), ''
        ).label('pin_list'),
        func.coalesce(func.count(pin.c.pin_name), 0).label('total'),
        global_list.c.list_name,
        global_list.c.list_desc,
        global_list.c.list_tag,
        global_list.c.created_at,
        user.c.username.label('created_by')
    ).join(
        global_list_pin_relation, global_list_pin_relation.c.list_id == global_list.c.id
    ).join(
        pin, pin.c.id == global_list_pin_relation.c.pin_id
    ).join(
        user, user.c.id == global_list.c.created_by
    )

    if search and search != '_all_':
        search = search.lower()
        query = query.filter(
            or_(
                func.lower(global_list.c.list_name).like(f"%{search}%"),
                func.lower(pin.c.pin_name).like(f"%{search}%"),
                func.lower(user.c.username).like(f"%{search}%"),
                func.lower(global_list.c.list_tag).like(f"%{search}%")
            )
        )

    query = query.group_by(global_list.c.id)
    query = query.order_by(global_list.c.created_at.desc())

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
            "count": 0
        }

async def get_pin_distance_by_coor(coor:str, userId:str):
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
        pin.c.created_by == userId,
    ).limit(10)

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