from services.modules.history.model import history
from sqlalchemy import insert, delete
from helpers.generator import get_UUID
from datetime import datetime
from datetime import datetime, timedelta

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

async def delete_all_expired_history(session):
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=200)

        # Query builder
        query = delete(history).where(history.c.created_at < cutoff_date)

        # Exec
        result = session.execute(query)
        session.commit()

        if result.rowcount > 0:
            return result.rowcount
        else:
            return None
    except Exception as e:
        session.rollback() 
        raise
    finally:
        session.close() 
