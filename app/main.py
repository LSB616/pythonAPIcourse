from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()
load_dotenv()

class Post(BaseModel):
    title:  str 
    content: str
    published: bool = True

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

my_posts = [{"title": "title of post 1", "content": "content of posts 1", "rating": 4, "id": 1}, {"title": "title of post 2", "content": "content of posts 2", "rating": 7, "id": 2}]

def find_post(id):
    for p in my_posts:
                if p["id"] == id:
                    return p

def find_index_post(id):
     for i, p in enumerate(my_posts):
          if p['id'] == id:
               return i

@app.get("/")
def root():
    return {"message": "Welcome to my FASTAPI"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (str(id)))
    post = cursor.fetchone()
    if not post:
         raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post With ID: {id} Was Not Found")
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post With ID: {id} Does Not Exist")
    return {"data": deleted_post}, Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post With ID: {id} Does Not Exist")
    return {"data": updated_post}