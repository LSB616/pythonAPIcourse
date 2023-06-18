from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URL"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#code for running Raw SQL

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# while True:
#     try:
#         conn = psycopg2.connect(host ='localhost', database ='fastapi', user='postgres', password=os.getenv("password"), cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database Connection Was Successful")
#         break
#     except Exception as error:
#         print("Connecting To Database Failed")
#         print("Error: ", error)
#         time.sleep(2)