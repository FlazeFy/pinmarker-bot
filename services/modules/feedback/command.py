from services.modules.feedback.model import feedback
from configs.configs import db
from sqlalchemy import insert, func
from helpers.generator import get_UUID
from fastapi import HTTPException
from datetime import datetime
from fastapi.responses import JSONResponse

async def post_feedback(data:dict):
    try:
        # Query builder
        feedback_rate = data.get('feedback_rate')
        feedback_body = data.get('feedback_body')
        created_at = datetime.utcnow()  # Use the current time

        if not isinstance(feedback_rate, int) or feedback_rate < 1 or feedback_rate > 5:
            raise HTTPException(status_code=400, detail="Invalid feedback_rate")
        if not isinstance(feedback_body, str) or len(feedback_body) > 500:
            raise HTTPException(status_code=400, detail="Invalid feedback_body")

        query = insert(feedback).values(
            id=get_UUID(),
            feedback_rate=feedback_rate,
            feedback_body=feedback_body,
            created_at=created_at
        )

        # Exec
        result = db.connect().execute(query)
        db.connect().commit()
        db.connect().close()

        if result.rowcount > 0:
            return JSONResponse(
                status_code=201, 
                content={
                    "message": "Feedback inserted",
                    "data": data,
                    "count": result.rowcount
                }
            )
        else:
            return JSONResponse(
                status_code=400, 
                content={
                    "data": None,
                    "message": "Feedback failed to insert",
                    "count": 0
                }
            )
    except Exception as e:
        db.connect().rollback()
        raise