from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to my FASTAPI"}

@app.get("/posts")
async def get_posts():
    return {"data": "List of Posts"}