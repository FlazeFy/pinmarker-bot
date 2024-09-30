from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import String,DateTime

history=Table(
    'history',meta,
    Column('id',String(36),primary_key=True),
    Column('history_type',String(36)),
    Column('history_context',String(255)),
    
    Column('created_at',DateTime),
    Column('created_by',String(36)),
)