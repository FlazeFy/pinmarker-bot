from bots.telegram.manual import send_tele_chat
from services.modules.user.admin_queries import get_all_admin_contact
from services.modules.user.user_queries import get_all_inactive_user

async def remind_user_inactive_every_week():
    # Fetch Admin Contact
    admins = await get_all_admin_contact()
    total_user = 0
    total_visit = 0

    # Fetch Review
    users = await get_all_inactive_user()
    if users:
        for idx, dt in enumerate(users):
            if dt.telegram_is_valid == 1 and dt.telegram_user_id:
                await send_tele_chat(
                    tele_id=dt.telegram_user_id,
                    msg=f"Hello {dt.username}, how was your day? we've already missing you. Your last login at Pinmarker about {dt.last_login.strftime('%d %m %Y')} who is about more than one months ago"
                )

        # Notify admins
        if admins:
            for admin in admins:
                await send_tele_chat(
                    tele_id=admin.telegram_user_id,
                    msg=f"[ADMIN] Hello {admin.username}, I just checked the user login history and found a total of {len(users)} users are likely inactive accounts."
                )