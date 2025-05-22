from services.modules.pin.pin_model import pin
from services.modules.pin.global_list_model import global_list
from services.modules.user.user_model import user
from configs.configs import db
from sqlalchemy import select, and_

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
        and_(
            global_list.c.list_tag.is_(None),
        )
    ).order_by(
        user.c.username.asc(),
        global_list.c.list_name.asc()
    )

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    if len(data) != 0:
        return data
    else:
        return None