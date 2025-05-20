from helpers.telegram.manual import send_tele_chat
from services.modules.user.admin_queries import get_all_admin_contact
from services.modules.visit.visit_queries import get_recap_all_weekly_visit

async def recap_summary_visit_history_every_week():
    # Fetch Admin Contact
    admins = await get_all_admin_contact()
    total_visit = 0
    total_user = 0

    # Fetch Visit History
    visits = await get_recap_all_weekly_visit()
    if visits:
        user_before = None
        visits_detail = ""
        user_visit_count = 0

        for idx, dt in enumerate(visits):
            if user_before != dt.username:
                # Telegram Bot Chat
                if user_before is not None:
                    total_user += 1
                    if dt.telegram_is_valid == 1:
                        await send_tele_chat(
                            tele_id=prev_tele_id,
                            msg=f"Hello {user_before}, for this week, we found that you have visited {user_visit_count} times. Here's the detail:\n\n{visits_detail}"
                        )
                
                # Reset For Different User
                user_before = dt.username
                visits_detail = ""
                user_visit_count = 0
                prev_tele_id = dt.telegram_user_id

            user_visit_count += 1
            total_visit += 1
            visit_with = f" with {dt.visit_with}" if dt.visit_with else ""
            visits_detail += f"- On <i>{dt.created_at.strftime('%d %m %Y %H:%M')}</i>, you visited <b>{dt.pin_name}</b> ({dt.pin_category}){visit_with} using {dt.visit_by}.\n"

            # Telegram Bot Chat for Last User
            if idx == len(visits) - 1:
                total_user += 1
                if dt.telegram_is_valid == 1:
                    await send_tele_chat(
                        tele_id=dt.telegram_user_id,
                        msg=f"Hello {dt.username}, for this week, we found that you have visited {user_visit_count} times. Here's the detail:\n\n{visits_detail}"
                    )

        # Notify admins
        if admins:
            for admin in admins:
                await send_tele_chat(
                    tele_id=admin.telegram_user_id,
                    msg=f"[ADMIN] Hello {admin.username}, I just checked the visit history and found a total of {total_visit} visits from {total_user} users this week."
                )
    else:
        if admins:
            for idx, dt in enumerate(admins):
                await send_tele_chat(tele_id=dt.telegram_user_id,msg=f"[ADMIN] Hello {dt.username}, I just checked the visit history, and there's no visit for this week")