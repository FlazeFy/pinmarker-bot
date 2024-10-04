from services.modules.pin.pin_model import pin
from services.modules.pin.global_list_model import global_list
from services.modules.visit.visit_model import visit
from services.modules.pin.global_list_rel_model import global_list_pin_relation
from services.modules.user.user_model import user
from services.modules.gallery.model import gallery
from configs.configs import db
from sqlalchemy import select, and_, func, or_, case
from sqlalchemy.sql.functions import concat
from helpers.converter import calculate_distance
from fastapi.responses import JSONResponse

async def get_all_pin(userId:str, platform:str):
    # Query builder
    if platform == 'telegram':
        query = select(
            pin.c.id,
            pin.c.pin_name,
            pin.c.pin_desc,
            concat(pin.c.pin_lat, ',', pin.c.pin_long).label('pin_coordinate'),
            pin.c.pin_category,
            pin.c.pin_person,
            pin.c.pin_address,
            pin.c.created_at,
            pin.c.is_favorite,
            func.ifnull(func.count(visit.c.id), 0).label('total_visit'),
            func.max(visit.c.created_at).label('last_visit')
        ).outerjoin(
            visit, visit.c.pin_id == pin.c.id
        ).where(
            pin.c.created_by == userId,
        ).group_by(
            pin.c.id
        ).order_by(
            pin.c.is_favorite.desc(),
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
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    if len(data) != 0:
        data_list = [dict(row._mapping) for row in data]
        data_list_final = []
        for row in data:
            data_list = dict(row._mapping)
            data_list['created_at'] = data_list['created_at'].isoformat() 
            if platform == 'telegram' and data_list['last_visit']:
                data_list['last_visit'] = data_list['last_visit'].isoformat() 
            data_list_final.append(data_list)
        data_list = data_list_final

        return JSONResponse(
            status_code=200, 
            content={
                "data": data_list,
                "message": "Pin found",
                "count": len(data)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "Pin not found",
                "count": 0
            }
        )
    
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
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    if len(data) != 0:
        data_list = [dict(row._mapping) for row in data]

        if platform != 'telegram':
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
                "message": "Pin found",
                "count": len(data)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "Pin not found",
                "count": 0
            }
        )
    
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
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    data_list = [dict(row._mapping) for row in data]

    if len(data) > 0:
        return JSONResponse(
            status_code=200, 
            content={
                "data": data_list,
                "message": "Pin found",
                "count": len(data)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "Pin not found",
                "count": 0
            }
        )
    
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
            
        return JSONResponse(
            status_code=200, 
            content={
                "data": data_list_final,
                "message": "Pin found",
                "count": len(data)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "Pin not found",
                "count": 0
            }
        )

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
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()
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
    
async def get_nearest_pin_query(lat:str, long:str, userid:str, max_dis:int,limit:int):
    # Query builder
    query = select(
        pin.c.pin_name,
        pin.c.pin_category,
        concat(pin.c.pin_lat, ',', pin.c.pin_long).label('pin_coordinate')
    ).where(
        pin.c.created_by == userid
    )

    #Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()
    found = False
    found_list = []

    for idx, dt in enumerate(data, start=1):
        my_coor = f"{lat},{long}"
        dis = calculate_distance(my_coor, dt.pin_coordinate)
        if dis < max_dis:
            found = True
            found_list.append({
                'pin_name': dt.pin_name,
                'pin_coor': dt.pin_coordinate,
                'pin_category': dt.pin_category,
                'distance': dis,
            })

        if len(found_list) >= limit:
            break

    found_list.sort(key=lambda dt: dt['distance'])

    if len(found_list) > 0:
        return JSONResponse(
            status_code=200, 
            content={
                "data": found_list,
                "message": "Pin found",
                "is_found_near": found,
                "count": len(found_list)
            }
        )
    else:
        return JSONResponse(
            status_code=404,
            content={
                "data": None,
                "message": "Pin not found",
                "is_found_near": found,
                "count": 0
            }
        )

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
        result_cat = db.connect().execute(query_cat)
        result_pin = db.connect().execute(query_pin)
        result_person = db.connect().execute(query_person)
        data_cat = result_cat.fetchall()
        data_pin = result_pin.fetchall()
        data_person = result_person.fetchall()
        db.connect().close()

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
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    data_list = [dict(row._mapping) for row in data]

    if len(data) > 0:
        return JSONResponse(
            status_code=200, 
            content={
                "data": data_list,
                "message": "Pin found",
                "count": len(data)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "Pin not found",
                "count": 0
            }
        )
    
async def get_detail_list_by_id_query(id:str, userId:str):
    # Query builder
    query_list = select(
        global_list.c.list_name,
        global_list.c.list_desc,
        global_list.c.list_tag,
        global_list.c.created_at,
        global_list.c.updated_at,
        user.c.username.label('created_by')
    ).where(
        and_(
            pin.c.created_by == userId,
            global_list.c.id == id
        )
    )

    query_list_rel = select(
        global_list_pin_relation.c.id,
        pin.c.pin_name,
        pin.c.pin_desc,
        pin.c.pin_lat,
        pin.c.pin_long,
        pin.c.pin_call,
        pin.c.pin_category,
        global_list_pin_relation.c.created_at,
        pin.c.pin_address,
        user.c.username.label('created_by'),
        func.ifnull(func.group_concat(func.coalesce(gallery.c.gallery_url, None)), '').label('gallery_url'),
        func.ifnull(func.group_concat(func.coalesce(gallery.c.gallery_caption, None)), '').label('gallery_caption'),
        func.ifnull(func.group_concat(func.coalesce(gallery.c.gallery_type, None)), '').label('gallery_type')
    ).join(
        pin, global_list_pin_relation.c.pin_id == pin.c.id
    ).join(
        user, user.c.id == global_list_pin_relation.c.created_by
    ).outerjoin(
        gallery, gallery.c.pin_id == pin.c.id
    ).where(
        global_list_pin_relation.c.list_id == id
    ).group_by(
        global_list_pin_relation.c.id
    ).order_by(
        global_list_pin_relation.c.created_at.desc()
    )

    #Exec
    result_detail = db.connect().execute(query_list)
    result_rel = db.connect().execute(query_list_rel)
    detail = result_detail.first()
    data = result_rel.fetchall()
    db.connect().close()

    if detail:
        detail_dict = dict(detail._mapping)
        detail_dict['created_at'] = detail_dict['created_at'].isoformat()
        if detail_dict['updated_at']:
            detail_dict['updated_at'] = detail_dict['updated_at'].isoformat()
        detail = detail_dict

    if data:
        data_dict_final = []
        for row in data:
            data_dict = dict(row._mapping)
            data_dict['created_at'] = data_dict['created_at'].isoformat() 
            data_dict_final.append(data_dict)
        data = data_dict_final

    if detail and data:
        return JSONResponse(
            status_code=200, 
            content={
                "detail": detail,
                "data": data,
                "message": "List and pin found",
                "count": len(data)
            }
        )
    elif detail: 
        return JSONResponse(
            status_code=200, 
            content={
                "detail": detail_dict,
                "data": None,
                "message": "List found",
                "count": 0
            }
        )
    else:
        return JSONResponse(
            status_code=404,
            content={
                "detail": None,
                "data": None,
                "message": "List not found",
                "count": 0
            }
        )
    
async def get_global_pin_by_list_id(list_ids:str):
    list_id_array = list(map(str, list_ids.split(',')))

    # Query builder
    query = select(
        global_list.c.id.label("list_id"),
        global_list.c.list_name,
        pin.c.pin_name,
        pin.c.pin_desc,
        pin.c.pin_category,
        concat(pin.c.pin_lat, ',', pin.c.pin_long).label('pin_coordinate'),
        global_list.c.created_at,
        user.c.username.label('created_by')
    ).join(
        global_list_pin_relation, global_list_pin_relation.c.list_id == global_list.c.id
    ).join(
        pin, pin.c.id == global_list_pin_relation.c.pin_id
    ).join(
        user, user.c.id == global_list.c.created_by
    ).where(
        and_(
            pin.c.deleted_at.is_(None),
            global_list.c.id.in_(list_id_array)
        )
    )

    # query = query.group_by(pin.c.id)
    query = query.order_by(global_list.c.created_at.desc())

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    data_list = [dict(row._mapping) for row in data]

    if len(data) > 0:
        data_list_final = []
        for row in data_list:
            row['created_at'] = row['created_at'].isoformat() 
            data_list_final.append(row)
            
        return JSONResponse(
            status_code=200, 
            content={
                "data": data_list_final,
                "message": "Pin found",
                "count": len(data)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "Pin not found",
                "count": 0
            }
        )
    
async def get_pin_detail_history_by_id(pin_id:str, user_id:str):
    # Query builder Detail
    query_detail = select(
        pin.c.pin_name,
        pin.c.pin_desc,
        pin.c.pin_category,
        pin.c.pin_lat,
        pin.c.pin_long,
        pin.c.pin_person,
        pin.c.pin_email,
        pin.c.pin_call,
        pin.c.pin_address,
        pin.c.created_at,
        pin.c.updated_at
    ).where(
        and_(
            pin.c.deleted_at.is_(None),
            pin.c.id == pin_id,
            pin.c.created_by == user_id
        )
    )

    # Exec Detail
    result_detail = db.connect().execute(query_detail)
    data_detail = result_detail.first()

    # Query builder visit
    data_history = []
    if data_detail:
        query_history = select(
            visit.c.visit_desc,
            visit.c.visit_by,
            visit.c.visit_with,
            visit.c.created_at,
        ).where(
            visit.c.pin_id == pin_id
        )

        # Exec visit
        result_history = db.connect().execute(query_history)
        data_history = result_history.fetchall()

    db.connect().close()

    if data_detail:
        data_detail_dict = dict(data_detail._mapping)
        data_detail_dict['created_at'] = data_detail_dict['created_at'].isoformat()
        if data_detail_dict['updated_at']:
            data_detail_dict['updated_at'] = data_detail_dict['updated_at'].isoformat()
        data_detail = data_detail_dict

        data_history_final = []
        data_history = [dict(row._mapping) for row in data_history]
        if data_history:
            for row in data_history:
                row['created_at'] = row['created_at'].isoformat() 
                data_history_final.append(row)

        return JSONResponse(
            status_code=200, 
            content={
                "data": data_detail,
                "message": "Pin found",
                "history": data_history_final if len(data_history_final) > 0 else None
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "Pin not found",
                "history": None
            }
        )
    
async def get_pin_distance_to_my_personal_pin_by_id(pin_id:str, user_id:str):
    # Query builder
    query = select(
        pin.c.id,
        pin.c.pin_name,
        pin.c.pin_desc,
        pin.c.pin_lat,
        pin.c.pin_long,
        pin.c.created_at,
    ).where(
        and_(
            pin.c.deleted_at.is_(None),
            pin.c.id != pin_id,
            pin.c.pin_category == 'Personal',
            pin.c.created_by == user_id
        )
    )
    # Exec Detail
    result = db.connect().execute(query)
    data = result.fetchall()

    if data:
        # Query departure
        query_departure = select(
            pin.c.pin_lat,
            pin.c.pin_long
        ).where(
            and_(
                pin.c.deleted_at.is_(None),
                pin.c.id == pin_id
            )
        )
        # Exec departure query
        result_departure = db.connect().execute(query_departure)
        data_departure = result_departure.first()

        db.connect().close()
        if data_departure:
            data_final = []
            data_list = [dict(row._mapping) for row in data]
            if data_list:
                for row in data_list:
                    row['created_at'] = row['created_at'].isoformat() 
                    row['distance_to_meters'] = float(round(calculate_distance(coord1=f"{row['pin_lat']},{row['pin_long']}", coord2=f"{data_departure.pin_lat},{data_departure.pin_long}"), 2))
                    data_final.append(row)
                    
            return JSONResponse(
                status_code=200, 
                content={
                    "data": data_final,
                    "message": "Pin found",
                    "count": len(data_final)
                }
            )
        else:
            return JSONResponse(
                status_code=404, 
                content={
                    "data": None,
                    "message": "Pin derpature not found",
                    "count": 0
                }
            )
    else:
        db.connect().close()
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "Pin not found",
                "count": 0
            }
        )
    
async def get_trash_pin(user_id:str):
    # Query builder
    query = select(
        pin.c.id,
        pin.c.pin_name,
        func.coalesce(func.count(visit.c.id), 0).label('total_visit'),
        pin.c.created_at,
        pin.c.updated_at,
        pin.c.deleted_at,
    ).outerjoin(
        visit, visit.c.pin_id == pin.c.id
    ).where(
        and_(
            pin.c.deleted_at.isnot(None),
            pin.c.created_by == user_id
        )
    ).group_by(
        pin.c.id
    ).order_by(
        pin.c.deleted_at.desc()
    )

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    data_list = [dict(row._mapping) for row in data]

    if len(data) > 0:
        data_list_final = []
        for row in data_list:
            row['created_at'] = row['created_at'].isoformat() 
            row['deleted_at'] = row['deleted_at'].isoformat() 
            if row['updated_at']:
                row['updated_at'] = row['updated_at'].isoformat() 
            data_list_final.append(row)
            
        return JSONResponse(
            status_code=200, 
            content={
                "data": data_list_final,
                "message": "Pin found",
                "count": len(data)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "Pin not found",
                "count": 0
            }
        )