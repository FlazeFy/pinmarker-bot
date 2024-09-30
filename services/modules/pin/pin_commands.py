from configs.configs import db
from services.modules.pin.pin_model import pin
from services.modules.history.command import create_history
from fastapi.responses import JSONResponse
from sqlalchemy import update, select
from datetime import datetime

async def soft_delete_pin_by_id(pin_id:str, user_id:str):
    try: 
        # Query builder
        query_update = (
            update(pin)
            .where(pin.c.id == pin_id)
            .where(pin.c.created_by == user_id)
            .where(pin.c.deleted_at.is_(None)) 
            .values(deleted_at=datetime.utcnow())
        )

        # Exec
        result_update = db.connect().execute(query_update)  
        db.connect().commit()

        if result_update.rowcount > 0:
            query_select = select(
                pin.c.pin_name,
            ).where(
                pin.c.id == pin_id
            )

            result_select = db.connect().execute(query_select)
            data_select = result_select.first()

            is_history_success = await create_history(
                type="Delete Marker",
                ctx=data_select.pin_name,
                user_id=user_id
            )

            if is_history_success:
                return JSONResponse(
                    status_code=201, 
                    content={
                        "message": "Pin deleted" if is_history_success else "Pin deleted but failed to write history",
                        "count": 1
                    }
                )
        else:
            db.connect().commit()
            db.connect().close()
            return JSONResponse(
                status_code=404, 
                content={
                    "message": "Pin not found",
                    "count": 0
                }
            )
    except Exception as e:
        db.connect().rollback()
        raise