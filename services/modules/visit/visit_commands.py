from configs.configs import db
from services.modules.visit.visit_model import visit
from services.modules.pin.pin_model import pin
from services.modules.user.user_model import user
from services.modules.history.command import create_history
from fastapi.responses import JSONResponse
from sqlalchemy import select, insert, and_
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from helpers.validator import validate_data
from helpers.generator import get_UUID

Session = sessionmaker(bind=db)

async def post_visit_query(data:dict):
    session = Session() 

    try: 
        pin_name = None

        # Query builder
        query_select = select(user.c.id).where(user.c.id == data.get('created_by'))
        result_select = session.execute(query_select)
        check_user = result_select.first()

        if check_user:
            if data.get('pin_id') != None and len(data.get('pin_id')) != 36: 
                return JSONResponse(status_code=422, content={"message": "Selected pin is have invalid id"})
            elif data.get('pin_id') != None and len(data.get('pin_id')) == 36: 
                query_select_pin = select(pin.c.pin_name).where(
                    and_(
                        pin.c.id == data.get('pin_id'),
                        pin.c.created_by == data.get('created_by')
                    )
                )
                result_select_pin = session.execute(query_select_pin)
                check_pin = result_select_pin.first()

                if check_pin is None:
                    return JSONResponse(status_code=404, content={"message": "Selected pin is not found"})
                else: 
                    pin_name = check_pin.pin_name

            # Command builder
            pin_id = data.get('pin_id')
            visit_desc = data.get('visit_desc')
            visit_by = data.get('visit_by')
            visit_with = data.get('visit_with')
            created_at = datetime.utcnow()
            created_by = data.get('created_by')
            id = get_UUID()

            errors_validation = []
            visit_desc_validate = validate_data(visit_desc, 'Visit Description', 'string', max_length=255, is_required=False)
            if visit_desc_validate:
                errors_validation = errors_validation + visit_desc_validate

            visit_by_validate = validate_data(visit_by, 'Visit By', 'string', max_length=75, is_required=True)
            if visit_by_validate:
                 errors_validation = errors_validation + visit_by_validate

            visit_with_validate = validate_data(visit_with, 'Visit With', 'string', max_length=500, min_length=3, is_required=False)
            if visit_with_validate:
                 errors_validation = errors_validation + visit_with_validate

            if errors_validation:
                return JSONResponse(status_code=422, content={"message": "Validation failed", "errors": errors_validation})

            query = insert(visit).values(
                id=id,
                pin_id=pin_id,
                visit_desc=visit_desc,
                visit_by=visit_by,
                visit_with=visit_with,
                created_at=created_at,
                created_by=created_by,
                updated_at=None,
            )

            # Exec
            result = session.execute(query)

            if result.rowcount > 0:
                data['id'] = id
                data['created_at'] = created_at.isoformat()
                if pin_name is not None:
                    data['pin_name'] = pin_name

                is_history_success = await create_history(
                    type="Add Visit",
                    ctx=visit_desc,
                    user_id=created_by,
                    session=session
                )

                session.commit()
                return JSONResponse(
                    status_code=201, 
                    content={
                        "message": "Visit created" if is_history_success else "Visit created but failed to write history",
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