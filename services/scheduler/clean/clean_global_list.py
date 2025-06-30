from bots.telegram.manual import send_tele_chat
from services.modules.user.admin_queries import get_all_admin_contact
from services.modules.pin.global_list_commands import delete_all_empty_expired_global_list
from sqlalchemy.orm import sessionmaker
from configs.configs import db

Session = sessionmaker(bind=db)

async def clean_empty_global_list_every_day():
    session = Session() 

    # Command Delete All Empty Expired Global List
    total_deleted = await delete_all_empty_expired_global_list(session=session)

    # Fetch Admin Contact
    admins = await get_all_admin_contact()

    if admins and total_deleted:
        for idx, dt in enumerate(admins):
            await send_tele_chat(msg=f"[ADMIN] Hello {dt.username}, I just checked the user's global list. And I just deleted about {total_deleted} user's empty global list that has been passed 100 days",tele_id=dt.telegram_user_id)
