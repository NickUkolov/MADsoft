from fastapi import FastAPI
from routes import memes

app = FastAPI()

app.include_router(memes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Meme API"}
