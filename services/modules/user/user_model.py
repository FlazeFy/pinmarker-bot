from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import String, Integer,DateTime

user=Table(
    'user',meta,
    Column('id',String(36),primary_key=True),
    Column('username',String(36)),
    Column('email',String(255)),
    Column('telegram_user_id',String(36)),
    Column('telegram_is_valid',Integer),
    Column('created_at',DateTime),
    Column('last_login',DateTime, nullable=True)
)