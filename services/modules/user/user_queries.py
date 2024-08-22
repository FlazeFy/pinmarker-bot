from services.modules.user.user_model import user
from services.modules.pin.pin_model import pin
from services.modules.user.admin_model import admin
from services.modules.dictionary.model import dictionary
from configs.configs import con
from sqlalchemy import select, and_, func
from sqlalchemy.sql.functions import coalesce

async def get_check_context_query(type:str, context:str):
    if type == "email":
        minChar = 10
        maxChar = 225
    elif type == "username":
        minChar = 6
        maxChar = 36

    if len(context) >= minChar and len(context) <= maxChar:
        # Query builder
        if type == "email":
            query = select(
                user.c.id,
            ).where(
                user.c.email == context,
            )
        elif type == "username":
            query = select(
                user.c.id,
            ).where(
                user.c.username == context,
            )

        # Exec
        result = con.execute(query)
        data = result.first()

        if data:
            return {
                "is_found": True,
                "message": f"{type} not available",
            }
        else:
            return {
                "is_found": False,
                "message": f"{type} available",
            }
    else:
        return {
            "message": f"{type} invalid, total character must more than {minChar} and below {maxChar}",
        }
    
async def get_profile_by_telegram_id(teleId:str):
    # Query builder - User
    query = select(
        user.c.id,
        user.c.username,
        user.c.email,
    ).where(
        and_(
            user.c.telegram_user_id == teleId,
            user.c.telegram_is_valid == 1
        )
    )

    # Exec - User
    result = con.execute(query)
    user_data = result.first()

    if user_data:
        return {
            "is_found": True,
            "role":"user",
            "data": user_data,
            "message":"User found"
        }
    else:
        # Query builder - Admin
        query = select(
            admin.c.id,
            admin.c.username,
            admin.c.email,
        ).where(
            and_(
                admin.c.telegram_user_id == teleId,
                admin.c.telegram_is_valid == 1
            )
        )

        # Exec - Admin
        result = con.execute(query)
        admin_data = result.first()
        
        if admin_data:
            return {
                "is_found": True,
                "role":"admin",
                "data": admin_data,
                "message":"Admin found"
            }
        else: 
            return {
                "is_found": False,
                "role": None,
                "data": None,
                "message": "Hello, This telegram account is not registered yet. Sync this telegram in https://pinmarker.leonardhors.com/MyProfileController",
            }
        
async def get_all_user():
    # Query builder
    pin_subquery = select(
        pin.c.created_by.label('user_id'),
        func.count(pin.c.id).label('total_pin')
    ).where(
        pin.c.deleted_at.is_(None)
    ).group_by(
        pin.c.created_by
    ).subquery()

    dictionary_subquery = select(
        dictionary.c.created_by.label('user_id'),
        func.count(dictionary.c.id).label('total_dictionary')
    ).group_by(
        dictionary.c.created_by
    ).subquery()

    query = select(
        user.c.id,
        user.c.username,
        user.c.email,
        user.c.telegram_user_id,
        user.c.telegram_is_valid,
        user.c.created_at,
        coalesce(pin_subquery.c.total_pin, 0).label('total_pin'),
        coalesce(dictionary_subquery.c.total_dictionary, 0).label('total_dictionary')
    ).outerjoin(
        pin_subquery, user.c.id == pin_subquery.c.user_id
    ).outerjoin(
        dictionary_subquery, user.c.id == dictionary_subquery.c.user_id
    ).group_by(
        user.c.id,
    ).order_by(
        user.c.username.asc()
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
       
        