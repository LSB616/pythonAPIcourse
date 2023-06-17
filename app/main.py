from fastapi import FastAPI
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
load_dotenv()

while True:
    try:
        conn = psycopg2.connect(host ='localhost', database ='fastapi', user='postgres', password=os.getenv("password"), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection Was Successful")
        break
    except Exception as error:
        print("Connecting To Database Failed")
        print("Error: ", error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)



@app.get("/")
def root():
    return {"message": "Welcome To My FASTAPI"}