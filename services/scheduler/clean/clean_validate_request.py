from bots.telegram.manual import send_tele_chat
from services.modules.user.admin_queries import get_all_admin_contact
from services.modules.user.validate_request_commands import delete_all_expired_validate_request
from sqlalchemy.orm import sessionmaker
from configs.configs import db

Session = sessionmaker(bind=db)

async def clean_expired_validate_request_every_day():
    session = Session() 

    # Command Delete All Expired Validate Request
    total_deleted = await delete_all_expired_validate_request(session=session)

    # Fetch Admin Contact
    admins = await get_all_admin_contact()

    if admins and total_deleted:
        for idx, dt in enumerate(admins):
            await send_tele_chat(msg=f"[ADMIN] Hello {dt.username}, I just checked the user's request. And I just deleted about {total_deleted} user's request that has been passed 2 days",tele_id=dt.telegram_user_id)
