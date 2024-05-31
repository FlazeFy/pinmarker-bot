from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String,DateTime,Boolean

pin=Table(
    'pin',meta,
    Column('id',String(36),primary_key=True),
    Column('pin_name',String(75)),
    Column('pin_desc',String(500), nullable=True),
    Column('pin_lat',String(144)),
    Column('pin_long',String(144)),
    Column('pin_category',String(36)),
    Column('pin_person',String(75), nullable=True),
    Column('pin_call',String(16), nullable=True),
    Column('pin_email',String(255), nullable=True),
    Column('pin_address',String(500), nullable=True),
    Column('is_favorite',Boolean),
    
    Column('created_at',DateTime),
    Column('created_by',String(36)),
    Column('updated_at',DateTime, nullable=True),
    Column('deleted_at',DateTime, nullable=True)
)