from services.modules.pin.pin_model import pin
from services.modules.visit.visit_model import visit
from services.modules.user.user_model import user
from services.modules.review.model import review
from configs.configs import db
from sqlalchemy import select
from datetime import datetime, timedelta

async def get_all_unreviewed_visit_pin():
    start_day = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=2)
    end_day = start_day + timedelta(days=1)

    # Query builder
    query = select(
        visit.c.visit_with,
        visit.c.created_at,
        pin.c.pin_name,
        user.c.username,
        user.c.telegram_is_valid,
        user.c.telegram_user_id
    ).outerjoin(
        review, review.c.visit_id == visit.c.id,
    ).join(
        user, user.c.id == visit.c.created_by
    ).join(
        pin, visit.c.pin_id == pin.c.id
    ).where(
        pin.c.deleted_at.is_(None),
        visit.c.created_at >= start_day,
        visit.c.created_at < end_day,
        review.c.review_person.is_(None),
        visit.c.visit_with.isnot(None)
    ).group_by(
        visit.c.id
    ).order_by(
        user.c.username.asc(),
        visit.c.created_at.asc()
    )

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    if len(data) != 0:
        return data
    else:
        return None

    