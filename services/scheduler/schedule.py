from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio

# Audit Scheduler
from services.scheduler.audit.audit_feedback import audit_show_all_feedback_every_week
# Recap Scheduler
from services.scheduler.recap.recap_visit import recap_summary_visit_history_every_week
# Clean Scheduler
from services.scheduler.clean.clean_history import clean_expired_history_every_day
from services.scheduler.clean.clean_validate_request import clean_expired_validate_request_every_day
# Remind Scheduler
from services.scheduler.remind.remind_review import remind_to_review_visited_pin_every_day
from services.scheduler.remind.remind_user import remind_user_inactive_every_week
from services.scheduler.remind.remind_global_list import remind_empty_tag_for_global_list_every_week

def start_scheduler():
    scheduler = BackgroundScheduler()

    # Run every friday at 00:10
    scheduler.add_job(
        lambda: asyncio.run(audit_show_all_feedback_every_week()),
        CronTrigger(day_of_week='fri', hour=0, minute=10),
        id="audit_show_all_feedback_every_week",
        replace_existing=True
    )

    # Run every day at 00:20
    scheduler.add_job(
        lambda: asyncio.run(clean_expired_history_every_day()),
        CronTrigger(hour=0, minute=20),
        id="clean_expired_history_every_day",
        replace_existing=True
    )

    # Run every day at 00:30
    scheduler.add_job(
        lambda: asyncio.run(clean_expired_validate_request_every_day()),
        CronTrigger(hour=0, minute=30),
        id="clean_expired_validate_request_every_day",
        replace_existing=True
    )
    scheduler.add_job(
        lambda: asyncio.run(remind_to_review_visited_pin_every_day()),
        CronTrigger(hour=0, minute=35),
        id="remind_to_review_visited_pin_every_day",
        replace_existing=True
    )

    # Run every tue and fri at 00:40
    scheduler.add_job(
        lambda: asyncio.run(remind_user_inactive_every_week()),
        CronTrigger(day_of_week='tue,fri', hour=0, minute=40),
        id="remind_user_inactive_every_week",
        replace_existing=True
    )
    # Run every mon and thu at 00:40
    scheduler.add_job(
        lambda: asyncio.run(remind_empty_tag_for_global_list_every_week()),
        CronTrigger(day_of_week='mon,thu',  hour=0, minute=40),
        id="remind_empty_tag_for_global_list_every_week",
        replace_existing=True
    )

    # Run every monday at 00:30
    scheduler.add_job(
        lambda: asyncio.run(recap_summary_visit_history_every_week()),
        CronTrigger(day_of_week='mon', hour=0, minute=30),
        id="recap_summary_visit_history_every_week",
        replace_existing=True
    )

    scheduler.start()