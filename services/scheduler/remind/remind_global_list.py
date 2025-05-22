from helpers.telegram.manual import send_tele_chat
from services.modules.user.admin_queries import get_all_admin_contact
from services.modules.pin.global_list_queries import get_all_empty_tag_for_global_list

async def remind_empty_tag_for_global_list_every_week():
    # Fetch Admin Contact
    admins = await get_all_admin_contact()
    total_user = 0
    total_list = 0

    # Fetch Review
    reviews = await get_all_empty_tag_for_global_list()
    if reviews:
        user_before = None
        global_list = ""

        for idx, dt in enumerate(reviews):
            if user_before != dt.username:
                # Telegram Bot Chat
                if user_before is not None:
                    total_user += 1
                    if dt.telegram_is_valid == 1:
                        await send_tele_chat(
                            tele_id=prev_tele_id,
                            msg=f"Hello {user_before}, I found that some of your global list of pin doesnt have at least one tag:\n\n{global_list}\nAttach a tag so you can find and group your pin easily based on your interest and also we can suggest the best place to visit next trip😉"
                        )
                
                # Reset For Different User
                user_before = dt.username
                global_list = ""
                prev_tele_id = dt.telegram_user_id

            total_list += 1
            global_list += f"- <b>{dt.list_name}</b>, created at <i>{dt.created_at.strftime('%d %m %Y %H:%M')}</i>.\n"

            # Telegram Bot Chat for Last User
            if idx == len(reviews) - 1:
                total_user += 1
                if dt.telegram_is_valid == 1:
                    await send_tele_chat(
                        tele_id=dt.telegram_user_id,
                        msg=f"Hello {user_before}, I found that some of your global list of pin doesnt have at least one tag:\n\n{global_list}\nAttach a tag so you can find and group your pin easily based on your interest and also we can suggest the best place to visit next trip😉"
                    )

        # Notify admins
        if admins:
            for admin in admins:
                await send_tele_chat(
                    tele_id=admin.telegram_user_id,
                    msg=f"[ADMIN] Hello {admin.username}, I just checked the global list and found a total of {total_list} list still doesnt have a tag, from {total_user} users this week."
                )