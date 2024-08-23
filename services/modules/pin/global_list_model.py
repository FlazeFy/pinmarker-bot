from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import String,DateTime,JSON

global_list=Table(
    'global_list',meta,
    Column('id',String(36),primary_key=True),
    Column('list_code',String(6), nullable=True),
    Column('list_name',String(75)),
    Column('list_desc',String(255), nullable=True),
    Column('list_tag',JSON, nullable=True),
    
    Column('created_at',DateTime),
    Column('created_by',String(36)),
    Column('updated_at',DateTime, nullable=True),
)