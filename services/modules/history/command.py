from configs.configs import db
from services.modules.history.model import history
from fastapi.responses import JSONResponse
from sqlalchemy import insert
from helpers.generator import get_UUID
from datetime import datetime

async def create_history(type: str, ctx: str, user_id: str, session):
    try:
        # Query builder
        query = insert(history).values(
            id=get_UUID(),
            history_type=type,
            history_context=ctx,
            created_by=user_id,
            created_at=datetime.utcnow()
        )

        # Exec
        result = session.execute(query)
        session.commit()

        if result.rowcount > 0:
            return True
        else:
            return False
    except Exception as e:
        session.rollback() 
        raise
    finally:
        session.close() 