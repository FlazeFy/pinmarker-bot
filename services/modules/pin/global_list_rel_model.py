from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import String,DateTime,JSON

global_list_pin_relation=Table(
    'global_list_pin_relation',meta,
    Column('id',String(36),primary_key=True),
    Column('pin_id',String(36)),
    Column('list_id',String(36)),
    
    Column('created_at',DateTime),
    Column('created_by',String(36)),
)