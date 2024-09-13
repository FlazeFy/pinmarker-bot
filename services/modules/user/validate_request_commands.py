from services.modules.user.validate_request_model import req
from services.modules.user.user_model import user
from helpers.mailer.mail import send_email
from helpers.generator import get_UUID, get_token_validation
from configs.configs import con
from datetime import datetime
from sqlalchemy import select, and_
from telegram import Bot
from helpers.telegram.manual import send_tele_chat

async def post_req_register_command(email:str, username:str, type:str):
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
    result = con.execute(query)
    data = result.first()

    if data is not None:
        return {
            "is_sended": False,
            "message": "Generate token failed. There's still a unvalidated request"
        }
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
        con.execute(new_request)
        con.commit()

        if type == 'register':
            message_body = f"Hello <b>{username}</b>, Thank you for using PinMarker for your location and places app management.<br><br>One step again to finish the registration process. Just copy this <h3>{token}</h3> and paste it to validation section in your registration page.<br><br>Thank You!"
            await send_email(
                subject="Account Registration",
                body=message_body,
                to_email=email
            )
            return {
                "is_sended": True,
                "message": "Token register is sended to your email!"
            }
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
            result2 = con.execute(query2)
            data = result2.first()

            if data.telegram_user_id:
                await send_tele_chat(tele_id=data.telegram_user_id,msg=message_body)

            return {
                "is_sended": True,
                "message": "Token password recovery is sended to your email!"
            }
        else:
            return {
                "is_sended": False,
                "message": "Type request not valid"
            }

async def post_validate_regis_command(token:str, username:str, type:str):
    # Query builder
    query = select(
        req.c.id,
    ).where(
        req.c.request_context == token,
        req.c.request_type == type,
        req.c.created_by == username
    )

    # Exec
    result = con.execute(query)
    data = result.first()

    if data is not None:
        # Command builder
        new_request = req.delete().where(
            req.c.id == data.id
        )

        total = con.execute(new_request)
        con.commit()

        if total.rowcount > 0:
            return {
                "is_validated": True,
                "message": "Token is validated!"
            }
        else:
            return {
                "is_validated": False,
                "message": "Token not found!"
            }
    else:
        return {
            "is_validated": False,
            "message": "Token not found!"
        }