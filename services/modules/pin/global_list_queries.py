from services.modules.pin.global_list_rel_model import global_list_pin_relation
from services.modules.pin.global_list_model import global_list
from services.modules.user.user_model import user
from configs.configs import db
from sqlalchemy import select

async def get_all_empty_tag_for_global_list():
    # Query builder
    query = select(
        global_list.c.list_name,
        global_list.c.created_at,
        user.c.username,
        user.c.telegram_is_valid,
        user.c.telegram_user_id
    ).join(
        user, user.c.id == global_list.c.created_by
    ).where(
        global_list.c.list_tag.is_(None),
    ).order_by(
        user.c.username.asc(),
        global_list.c.created_at.desc()
    )

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    if len(data) != 0:
        return data
    else:
        return None
    

async def get_all_empty_global_list():
    # Query builder
    query = select(
        global_list.c.list_name,
        global_list.c.created_at,
        user.c.username,
        user.c.telegram_is_valid,
        user.c.telegram_user_id
    ).join(
        user, user.c.id == global_list.c.created_by
    ).outerjoin(
        global_list_pin_relation, global_list.c.id == global_list_pin_relation.c.list_id
    ).where(
        global_list_pin_relation.c.list_id.is_(None),
    ).group_by(
        global_list.c.id
    ).order_by(
        user.c.username.asc(),
        global_list.c.created_at.desc()
    )

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    if len(data) != 0:
        return data
    else:
        return None