from services.modules.user.user_model import user
from services.modules.user.admin_model import admin
from configs.configs import con
from sqlalchemy import select, and_

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
       
        