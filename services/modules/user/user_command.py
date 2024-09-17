from services.modules.user.user_model import user
from services.modules.user.admin_model import admin
from configs.configs import db
from sqlalchemy import update
from fastapi.responses import JSONResponse

async def update_sign_out(userId:str, teleId:str, role:str):
    try: 
        # Query builder - User
        stmt = update(user
            ).where(
                user.c.id == userId,
                user.c.telegram_user_id == teleId
            ).values(
                telegram_user_id=None,
                telegram_is_valid=0
            )
        
        # Exec - User
        result = db.connect().execute(stmt)
        db.connect().commit()
        
        if result.rowcount > 0:
            return JSONResponse(
                status_code=201, 
                content={
                    "is_updated": True,
                    "message": "User successfully sign out"
                }
            )
        else:
            # Query builder - Admin
            stmt = update(admin
                ).where(
                    admin.c.id == userId,
                    admin.c.telegram_user_id == teleId
                ).values(
                    telegram_user_id=None,
                    telegram_is_valid=0
                )
            
            # Exec - Admin
            result = db.connect().execute(stmt)
            db.connect().commit()
            db.connect().close()

            if result.rowcount > 0:
                return JSONResponse(
                    status_code=201, 
                    content={
                            "is_updated": True,
                            "message": "Admin successfully sign out"
                        }
                )
            else:
                return JSONResponse(
                    status_code=404, 
                    content={
                        "is_updated": False,
                        "message": "No user found with the provided Telegram Id"
                    }
                )
    except Exception as e:
        db.connect().rollback()
        raise
       
        