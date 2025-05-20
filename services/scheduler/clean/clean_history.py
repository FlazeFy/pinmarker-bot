from helpers.telegram.manual import send_tele_chat
from services.modules.user.admin_queries import get_all_admin_contact
from services.modules.history.command import delete_all_expired_history
from sqlalchemy.orm import sessionmaker
from configs.configs import db

Session = sessionmaker(bind=db)

async def clean_expired_history_every_day():
    session = Session() 

    # Command Delete All Expired History
    total_deleted = await delete_all_expired_history(session=session)

    # Fetch Admin Contact
    admins = await get_all_admin_contact()

    if admins and total_deleted:
        for idx, dt in enumerate(admins):
            await send_tele_chat(msg=f"[ADMIN] Hello {dt.username}, I just checked the system history. And I just deleted about {total_deleted} history that has been passed 30 days",tele_id=dt.telegram_user_id)
