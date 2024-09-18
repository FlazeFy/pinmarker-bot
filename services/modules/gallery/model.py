from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import String,DateTime

gallery=Table(
    'gallery',meta,
    Column('id',String(36),primary_key=True),
    Column('pin_id',String(36)),
    Column('gallery_type',String(14)),
    Column('gallery_url',String(1000)),
    Column('gallery_caption',String(500)),
    
    Column('created_at',DateTime),
    Column('created_by',String(36))
)