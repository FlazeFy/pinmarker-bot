from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio

# Audit Scheduler
from services.scheduler.audit.audit_feedback import audit_show_all_feedback_every_week

def start_scheduler():
    scheduler = BackgroundScheduler()

    # Run every friday at 00:10
    scheduler.add_job(
        lambda: asyncio.run(audit_show_all_feedback_every_week()),
        CronTrigger(day_of_week='fri', hour=0, minute=10),
        id="audit_show_all_feedback_every_week",
        replace_existing=True
    )

    scheduler.start()