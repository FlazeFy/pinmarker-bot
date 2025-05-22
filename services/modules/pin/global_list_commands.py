from sqlalchemy import delete, select
from datetime import datetime
from services.modules.pin.global_list_model import global_list
from services.modules.pin.global_list_rel_model import global_list_pin_relation
from datetime import datetime, timedelta

async def delete_all_empty_expired_global_list(session):
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=100)

        # Query builder : Get Expired Global List
        list_expired_query = select(
            global_list.c.id,
        ).outerjoin(
            global_list_pin_relation, global_list.c.id == global_list_pin_relation.c.list_id
        ).where(
            global_list_pin_relation.c.list_id.is_(None),
            global_list.c.created_at < cutoff_date
        ).group_by(
            global_list.c.id
        ).order_by(
            global_list.c.created_at.desc()
        )

        # Query builder : Delete List Of Expired
        result = session.execute(list_expired_query)
        expired_ids = [row.id for row in result.fetchall()]

        if expired_ids:
            delete_query = delete(global_list).where(
                global_list.c.id.in_(expired_ids)
            )
            delete_result = session.execute(delete_query)
            session.commit()
            
            return delete_result.rowcount

        return 0
    except Exception as e:
        session.rollback() 
        raise
    finally:
        session.close() 