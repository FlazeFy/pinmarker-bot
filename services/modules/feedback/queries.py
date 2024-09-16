from services.modules.feedback.model import feedback
from configs.configs import db
from sqlalchemy import select
    
async def get_feedback():
    # Query builder
    query = select(
        feedback.c.feedback_rate,
        feedback.c.feedback_body,
        feedback.c.created_at
    ).order_by(
        feedback.c.created_at.desc()
    )

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    data_list = [dict(row._mapping) for row in data]

    if len(data) > 0:
        return {
            "data": data_list,
            "message": "Feedback found",
            "count": len(data)
        }
    else:
        return {
            "data": None,
            "message": "Feedback not found",
        }