from services.modules.user.validate_request_model import req
from helpers.mailer.mail import send_email
from helpers.generator import get_UUID, get_token_validation
from configs.configs import con
from datetime import datetime
from sqlalchemy import select

async def post_req_register_command(email:str, username:str):
    # Query builder
    query = select(
        req.c.id,
    ).where(
        req.c.request_type == 'register',
        req.c.created_by == username
    )
    # Exec
    result = con.execute(query)
    data = result.first()

    if data is not None:
        return {
            "message": "Generate token failed. There's still a unvalidated request"
        }
    else:
        id = get_UUID()
        token = get_token_validation(length=6)

        # Command builder
        new_request = req.insert().values(
            id=id,
            request_type='register',
            request_context=token,
            created_at=datetime.utcnow(),
            created_by=username
        )
        con.execute(new_request)
        con.commit()

        # Send email
        message_body = f"Hello <b>{username}</b>, Thank you for using PinMarker for your location and places app management.<br><br>One step again to finish the registration process. Just copy this <h3>{token}</h3>and paste it to validation section in your registration page.<br><br>Thank You!"

        await send_email(
            subject="Account Registration",
            body=message_body,
            to_email=email
        )

        return {
            "message": "Token register is sended to your email!"
        }

async def post_validate_regis_command(token:str, username:str):
    # Query builder
    query = select(
        req.c.id,
    ).where(
        req.c.request_context == token,
        req.c.request_type == 'register',
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