from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import String, DateTime

req=Table(
    'validate_request',meta,
    Column('id',String(36),primary_key=True),
    Column('request_type',String(36)),
    Column('request_context',String(75)),
    Column('created_at',DateTime),
    Column('created_by',String(36)),
)