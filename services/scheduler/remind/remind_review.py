from bots.telegram.manual import send_tele_chat
from services.modules.user.admin_queries import get_all_admin_contact
from services.modules.review.queries import get_all_unreviewed_visit_pin

async def remind_to_review_visited_pin_every_day():
    # Fetch Admin Contact
    admins = await get_all_admin_contact()
    total_user = 0
    total_visit = 0

    # Fetch Review
    reviews = await get_all_unreviewed_visit_pin()
    if reviews:
        user_before = None
        reviews_detail = ""

        for idx, dt in enumerate(reviews):
            if user_before != dt.username:
                # Telegram Bot Chat
                if user_before is not None:
                    total_user += 1
                    if dt.telegram_is_valid == 1:
                        await send_tele_chat(
                            tele_id=prev_tele_id,
                            msg=f"Hello {user_before}, how was your experience for last visit 2 days ago at:\n\n{reviews_detail}\nTell us your experience in our Apps. So in the future we know what kind of your favorite place and maybe give you suggestion for next trip"
                        )
                
                # Reset For Different User
                user_before = dt.username
                reviews_detail = ""
                prev_tele_id = dt.telegram_user_id

            total_visit += 1
            reviews_detail += f"- <b>{dt.pin_name}</b> with {dt.visit_with}, at <i>{dt.created_at.strftime('%d %m %Y %H:%M')}</i>.\n"

            # Telegram Bot Chat for Last User
            if idx == len(reviews) - 1:
                total_user += 1
                if dt.telegram_is_valid == 1:
                    await send_tele_chat(
                        tele_id=dt.telegram_user_id,
                        msg=f"Hello {user_before}, how was your experience for last visit 2 days ago at:\n\n{reviews_detail}\nTell us your experience in our Apps. So in the future we know what kind of your favorite place and maybe give you suggestion for next trip"
                    )

        # Notify admins
        if admins:
            for admin in admins:
                await send_tele_chat(
                    tele_id=admin.telegram_user_id,
                    msg=f"[ADMIN] Hello {admin.username}, I just checked the visit history and found a total of {total_visit} vist has not been reviewed yet, from {total_user} users this week."
                )