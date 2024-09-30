from configs.configs import db
from services.modules.history.model import history
from fastapi.responses import JSONResponse
from sqlalchemy import insert
from helpers.generator import get_UUID
from datetime import datetime

async def create_history(type:str, ctx:str, user_id:str):
    # Query builder
    query = (
        insert(history)
        .values(
            id=get_UUID(),
            history_type=type,
            history_context=ctx,
            created_by=user_id,
            created_at=datetime.utcnow()
        )
    )

    # Exec
    result = db.connect().execute(query)
    db.connect().commit()
    db.connect().close()

    if result.rowcount > 0:
        return True
    else:
        return False