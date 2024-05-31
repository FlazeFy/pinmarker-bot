from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String,DateTime,Boolean

visit=Table(
    'visit',meta,
    Column('id',String(36),primary_key=True),
    Column('pin_id',String(36)),
    Column('visit_desc',String(255), nullable=True),
    Column('visit_by',String(75)),
    Column('visit_with',String(500), nullable=True),
    
    Column('created_at',DateTime),
    Column('created_by',String(36)),
    Column('updated_at',DateTime, nullable=True),
)