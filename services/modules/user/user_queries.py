from services.modules.user.user_model import user
from configs.configs import con
from sqlalchemy import select

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
    # Query builder
    query = select(
        user.c.id,
        user.c.username,
        user.c.email,
    ).where(
        user.c.telegram_user_id == teleId
    )

    # Exec
    result = con.execute(query)
    data = result.first()

    if data:
        return {
            "is_found": True,
            "data": data,
            "message":"User found"
        }
    else:
        return {
            "is_found": False,
            "data": None,
            "message": "Hello, This telegram account is not registered yet. Sync this telegram in https://pinmarker.leonardhors.com/MyProfileController",
        }
       
        