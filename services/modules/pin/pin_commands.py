from configs.configs import db
from services.modules.pin.pin_model import pin
from services.modules.history.command import create_history
from fastapi.responses import JSONResponse
from sqlalchemy import update, select, delete
from datetime import datetime
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db)

async def soft_delete_pin_by_id(pin_id: str, user_id: str):
    session = Session() 

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
        result_update = session.execute(query_update)

        if result_update.rowcount > 0:
            query_select = select(pin.c.pin_name).where(pin.c.id == pin_id)
            result_select = session.execute(query_select)
            data_select = result_select.first()

            if data_select:
                is_history_success = await create_history(
                    type="Delete pin",
                    ctx=data_select.pin_name,
                    user_id=user_id,
                    session=session
                )

                session.commit()
                return JSONResponse(
                    status_code=201, 
                    content={
                        "message": "Pin deleted" if is_history_success else "Pin deleted but failed to write history",
                        "count": 1
                    }
                )
        else:
            session.commit()
            return JSONResponse(
                status_code=404, 
                content={
                    "message": "Pin not found",
                    "count": 0
                }
            )
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close() 

async def recover_pin_by_id(pin_id: str, user_id: str):
    session = Session() 

    try: 
        # Query builder
        query_update = (
            update(pin)
            .where(pin.c.id == pin_id)
            .where(pin.c.created_by == user_id)
            .where(pin.c.deleted_at.isnot(None))
            .values(deleted_at = None)
        )

        # Exec
        result_update = session.execute(query_update)

        if result_update.rowcount > 0:
            query_select = select(pin.c.pin_name).where(pin.c.id == pin_id)
            result_select = session.execute(query_select)
            data_select = result_select.first()

            if data_select:
                is_history_success = await create_history(
                    type="Recover pin",
                    ctx=data_select.pin_name,
                    user_id=user_id,
                    session=session
                )

                session.commit()
                return JSONResponse(
                    status_code=201, 
                    content={
                        "message": "Pin recovered" if is_history_success else "Pin recovered but failed to write history",
                        "count": 1
                    }
                )
        else:
            session.commit()
            return JSONResponse(
                status_code=404, 
                content={
                    "message": "Pin not found",
                    "count": 0
                }
            )
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close() 

async def hard_delete_pin_by_id(pin_id: str, user_id: str):
    session = Session() 

    try: 
        # Query builder
        query_select = select(pin.c.pin_name).where(pin.c.id == pin_id)
        result_select = session.execute(query_select)
        data_select = result_select.first()

        if data_select:
            query_update = (
                delete(pin)
                .where(pin.c.id == pin_id)
                .where(pin.c.created_by == user_id)
                .where(pin.c.deleted_at.isnot(None))
            )

            # Exec
            result_update = session.execute(query_update)
            
            if result_update.rowcount > 0:
                is_history_success = await create_history(
                    type="Permentally delete pin",
                    ctx=data_select.pin_name,
                    user_id=user_id,
                    session=session
                )

                session.commit()
                return JSONResponse(
                    status_code=201, 
                    content={
                        "message": "Pin permentally deleted" if is_history_success else "Pin permentally deleted but failed to write history",
                        "count": 1
                    }
                )
            else: 
                session.commit()
                return JSONResponse(
                    status_code=404, 
                    content={
                        "message": "Pin not found",
                        "count": 0
                    }
                )
        else:
            session.commit()
            return JSONResponse(
                status_code=404, 
                content={
                    "message": "Pin not found",
                    "count": 0
                }
            )
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close() 