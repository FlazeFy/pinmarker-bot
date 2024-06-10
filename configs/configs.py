from sqlalchemy import create_engine,MetaData
from firebase_admin import credentials
import firebase_admin

# MySQL
engine=create_engine('mysql+pymysql://root@localhost:3306/pinmarker')
meta=MetaData()
con=engine.connect()

# Firebase
cred = credentials.Certificate("configs/pinmarker-36552-firebase-adminsdk-5dett-b688b092f1.json")
