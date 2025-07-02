from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import String,DateTime

bot_relation=Table(
    'bot_relation',meta,
    Column('id',String(36),primary_key=True),
    Column('context_id',String(255)),
    Column('relation_type',String(36)),
    Column('relation_platform',String(14)),
    Column('relation_name',String(144)),
    Column('created_at',DateTime),
    Column('created_by',String(36)),
    Column('expired_at',DateTime),
)