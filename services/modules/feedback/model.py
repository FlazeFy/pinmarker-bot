from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String,DateTime

feedback=Table(
    'feedback',meta,
    Column('id',String(36),primary_key=True),
    Column('feedback_rate',Integer),
    Column('feedback_body',String(500)),
    Column('created_at',DateTime)
)