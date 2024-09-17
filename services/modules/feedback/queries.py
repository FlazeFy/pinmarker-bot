from services.modules.feedback.model import feedback
from configs.configs import db
from sqlalchemy import select
from fastapi.responses import JSONResponse

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

    data_list = []
    for row in data:
        feedback_dict = dict(row._mapping)
        feedback_dict['created_at'] = feedback_dict['created_at'].isoformat() 
        data_list.append(feedback_dict)

    if len(data) > 0:
        return JSONResponse(
            status_code=200, 
            content={
                "data": data_list,
                "message": "Feedback found",
                "count": len(data)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "Feedback not found",
                "count": 0
            }
        )