from services.modules.user.validate_request_model import req
from services.modules.user.user_model import user
from helpers.mailer.mail import send_email
from helpers.generator import get_UUID, get_token_validation
from configs.configs import db
from datetime import datetime, timedelta
from sqlalchemy import select, and_, delete
from bots.telegram.manual import send_tele_chat
from fastapi.responses import JSONResponse

async def post_req_register_command(email:str, username:str, type:str):
    try: 
        # Query builder
        query = select(
            req.c.id,
        ).where(
            and_(
                req.c.request_type == type,
                req.c.created_by == username
            )
        )
        # Exec
        result = db.connect().execute(query)
        data = result.first()

        if data is not None:
            return JSONResponse(
                status_code=409, 
                content={
                    "is_sended": False,
                    "message": "Generate token failed. There's still a unvalidated request"
                }
            )
        else:
            id = get_UUID()
            token = get_token_validation(length=6)

            # Command builder
            new_request = req.insert().values(
                id=id,
                request_type=type,
                request_context=token,
                created_at=datetime.utcnow(),
                created_by=username
            )
            db.connect().execute(new_request)
            db.connect().commit()

            if type == 'register':
                db.connect().close()
                message_body = f"Hello <b>{username}</b>, Thank you for using PinMarker for your location and places app management.<br><br>One step again to finish the registration process. Just copy this <h3>{token}</h3> and paste it to validation section in your registration page.<br><br>Thank You!"
                await send_email(
                    subject="Account Registration",
                    body=message_body,
                    to_email=email
                )
                return JSONResponse(
                    status_code=201, 
                    content={
                        "is_sended": True,
                        "message": "Token register is sended to your email!"
                    }
                )
            elif type == 'forget':
                message_body = f"Hello <b>{username}</b>, Here's the token for your password recovery. Just copy this <b>{token}</b> and paste it to validation section in your forget password page.\n\nThank You!"
                await send_email(
                    subject="Password Recovery",
                    body=message_body,
                    to_email=email
                )
                # Query builder
                query2 = select(
                    user.c.telegram_user_id,
                ).where(
                    user.c.telegram_is_valid == 1,
                    user.c.username == username
                )
                # Exec
                result2 = db.connect().execute(query2)
                data = result2.first()
                db.connect().close()

                if data.telegram_user_id:
                    await send_tele_chat(tele_id=data.telegram_user_id,msg=message_body)

                return JSONResponse(
                    status_code=201, 
                    content={
                        "is_sended": True,
                        "message": "Token password recovery is sended to your email!"
                    }
                )
            else:
                db.connect().close()
                return JSONResponse(
                    status_code=422, 
                    content={
                        "is_sended": False,
                        "message": "Type request not valid"
                    }
                )
    except Exception as e:
        db.connect().rollback()
        raise

async def post_validate_regis_command(token:str, username:str, type:str):
    try :
        # Query builder
        query = select(
            req.c.id,
        ).where(
            req.c.request_context == token,
            req.c.request_type == type,
            req.c.created_by == username
        )

        # Exec
        result = db.connect().execute(query)
        data = result.first()

        if data is not None:
            # Command builder
            new_request = req.delete().where(
                req.c.id == data.id
            )

            total = db.connect().execute(new_request)
            db.connect().commit()
            db.connect().close()

            if total.rowcount > 0:
                return JSONResponse(
                    status_code=201, 
                    content={
                        "is_validated": True,
                        "message": "Token is validated!"
                    }
                )
            else:
                return JSONResponse(
                    status_code=404, 
                    content={
                        "is_validated": False,
                        "message": "Token not found!"
                    }
                )
        else:
            db.connect().close()
            return JSONResponse(
                status_code=404, 
                content={
                    "is_validated": False,
                    "message": "Token not found!"
                }
            )
    except Exception as e:
        db.connect().rollback()
        raise

async def delete_all_expired_validate_request(session):
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=2)

        # Query builder
        query = delete(req).where(req.c.created_at < cutoff_date)

        # Exec
        result = session.execute(query)
        session.commit()

        if result.rowcount > 0:
            return result.rowcount
        else:
            return None
    except Exception as e:
        session.rollback() 
        raise
    finally:
        session.close() 