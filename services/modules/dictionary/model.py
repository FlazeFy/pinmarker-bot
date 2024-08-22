from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import String

dictionary=Table(
    'dictionary',meta,
    Column('id',String(36),primary_key=True),
    Column('dictionary_type',String(36)),
    Column('dictionary_name',String(36)),
    Column('dictionary_color',String(36)),
    Column('created_by',String(36))
)