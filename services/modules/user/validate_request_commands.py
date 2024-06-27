from services.modules.user.validate_request_model import req
from helpers.mailer.mail import send_email
from helpers.generator import get_UUID, get_token_validation
from configs.configs import con
from datetime import datetime

async def post_req_register_command(email:str, username:str):
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
        "message": "Request inserted successfully"
    }