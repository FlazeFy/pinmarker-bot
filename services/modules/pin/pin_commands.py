from configs.configs import db
from services.modules.pin.pin_model import pin
from services.modules.user.user_model import user
from services.modules.history.command import create_history
from fastapi.responses import JSONResponse
from sqlalchemy import update, select, delete, insert
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from helpers.validator import validate_data
from helpers.generator import get_UUID

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
                    status_code=200, 
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
                    status_code=200, 
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
                    status_code=200, 
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

async def put_pin_favorite(pin_id: str, user_id: str):
    session = Session() 

    try: 
        # Query builder
        query_select = select(pin.c.is_favorite).where(pin.c.id == pin_id)
        result_select = session.execute(query_select)
        data_select = result_select.first()

        if data_select:
            query_update = (
                update(pin)
                .where(pin.c.id == pin_id)
                .where(pin.c.created_by == user_id)
                .values(is_favorite=1 if data_select.is_favorite == 0 else 0)
            )

            # Exec
            result_update = session.execute(query_update)
            
            if result_update.rowcount > 0:
                session.commit()
                return JSONResponse(
                    status_code=200, 
                    content={
                        "message": "Pin updated",
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

async def post_pin_query(data:dict):
    session = Session() 

    try: 
        # Query builder
        query_select = select(user.c.id).where(user.c.id == data.get('created_by'))
        result_select = session.execute(query_select)
        check_user = result_select.first()

        if check_user:
            # Command builder
            pin_name = data.get('pin_name')
            pin_desc = data.get('pin_desc')
            pin_lat = data.get('pin_lat')
            pin_long = data.get('pin_long')
            pin_category = data.get('pin_category')
            pin_person = data.get('pin_person')
            pin_call = data.get('pin_call')
            pin_email = data.get('pin_email')
            pin_address = data.get('pin_address')
            is_favorite = data.get('is_favorite')
            created_at = data.get('created_at') or datetime.utcnow()
            created_by = data.get('created_by')
            id = get_UUID()

            errors_validation = []
            pin_name_validate = validate_data(pin_name, 'Pin Name', 'string', max_length=75, min_length=2, is_required=True)
            if pin_name_validate:
                errors_validation = errors_validation + pin_name_validate

            pin_desc_validate = validate_data(pin_desc, 'Pin Description', 'string', max_length=500, is_required=False)
            if pin_desc_validate:
                 errors_validation = errors_validation + pin_desc_validate

            pin_lat_validate = validate_data(pin_lat, 'Pin Latitude', 'string', max_length=144, min_length=3, is_required=True)
            if pin_lat_validate:
                 errors_validation = errors_validation + pin_lat_validate

            pin_long_validate = validate_data(pin_long, 'Pin Longitude', 'string', max_length=144, min_length=3, is_required=True)
            if pin_long_validate:
                 errors_validation = errors_validation + pin_long_validate

            pin_category_validate = validate_data(pin_category, 'Pin Category', 'string', max_length=36, is_required=True)
            if pin_category_validate:
                 errors_validation = errors_validation + pin_category_validate

            pin_person_validate = validate_data(pin_person, 'Pin Person', 'string', max_length=75, is_required=False)
            if pin_person_validate:
                 errors_validation = errors_validation + pin_person_validate

            pin_call_validate = validate_data(pin_call, 'Pin Call', 'string', max_length=16, is_required=False)
            if pin_call_validate:
                 errors_validation = errors_validation + pin_call_validate

            pin_email_validate = validate_data(pin_email, 'Pin Email', 'string', max_length=255, min_length=9, is_required=False)
            if pin_email_validate:
                 errors_validation = errors_validation + pin_email_validate

            pin_address_validate = validate_data(pin_address, 'Pin Address', 'string', max_length=500, is_required=False)
            if pin_address_validate:
                 errors_validation = errors_validation + pin_address_validate

            if errors_validation:
                return JSONResponse(status_code=422, content={"message": "Validation failed", "errors": errors_validation})

            query = insert(pin).values(
                id=id,
                pin_name=pin_name,
                pin_desc=pin_desc,
                pin_lat=pin_lat,
                pin_long=pin_long,
                pin_category=pin_category,
                pin_person=pin_person,
                pin_call=pin_call,
                pin_email=pin_email,
                pin_address=pin_address,
                is_favorite=is_favorite,
                created_at=created_at,
                created_by=created_by,
                updated_at=None,
                deleted_at=None 
            )

            # Exec
            result = session.execute(query)

            if result.rowcount > 0:
                data['id'] = id
                data['created_at'] = created_at.isoformat()

                is_history_success = await create_history(
                    type="Add Marker",
                    ctx=pin_name,
                    user_id=created_by,
                    session=session
                )

                session.commit()
                return JSONResponse(
                    status_code=201, 
                    content={
                        "message": "Pin created" if is_history_success else "Pin created but failed to write history",
                        "data": data,
                        "count": result.rowcount
                    }
                )
            else:
                return JSONResponse(
                    status_code=400, 
                    content={
                        "data": None,
                        "message": "Something error! Please call admin",
                        "count": 0
                    }
                )
        else:
            return JSONResponse(
                status_code=401, 
                content={
                    "data": None,
                    "message": "User account not found",
                }
            )
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close() 