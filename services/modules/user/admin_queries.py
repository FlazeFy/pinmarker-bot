from services.modules.user.admin_model import admin
from configs.configs import db
from sqlalchemy import select
        
async def get_all_admin_contact():
    # Query builder
    query = select(
        admin.c.username,
        admin.c.email,
        admin.c.telegram_user_id
    ).where(
        admin.c.telegram_is_valid != 0,
        admin.c.telegram_user_id.isnot(None)
    )

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    if len(data) != 0:
        return data
    else:
        return None