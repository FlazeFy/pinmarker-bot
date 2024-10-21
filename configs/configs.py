from sqlalchemy import create_engine,MetaData
from firebase_admin import credentials

# MySQL
db=create_engine('mysql+pymysql://root@localhost:3306/pinmarker', pool_size=20, max_overflow=80, pool_pre_ping=True, pool_recycle=100000)
meta=MetaData()

# Firebase
cred = credentials.Certificate("configs/pinmarker-36552-firebase-adminsdk-5dett-b688b092f1.json")
