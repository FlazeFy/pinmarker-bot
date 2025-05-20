from configs.configs import meta
from sqlalchemy import Integer, Table,Column
from sqlalchemy.sql.sqltypes import String,DateTime

review=Table(
    'review',meta,
    Column('id',String(36),primary_key=True),
    Column('visit_id',String(36)),
    Column('review_person',String(36)),
    Column('review_rate',Integer),
    Column('review_body',String(255), nullable=True),
    
    Column('created_at',DateTime),
    Column('created_by',String(36)),
)