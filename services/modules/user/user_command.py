from services.modules.user.user_model import user
from configs.configs import con
from sqlalchemy import update
    
async def update_sign_out(userId:str, teleId:str):
    # Query builder
    stmt = update(user
        ).where(
            user.c.id == userId,
            user.c.telegram_user_id == teleId
        ).values(
            telegram_user_id=None,
            telegram_is_valid=0
        )
    
    # Exec
    result = con.execute(stmt)
    con.commit()
    
    if result.rowcount > 0:
        return {
            "is_updated": True,
            "message": "User successfully sign out"
        }
    else:
        return {
            "is_updated": False,
            "message": "No user found with the provided Telegram Id"
        }
       
        