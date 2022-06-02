from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()


@app.get("/")
def index_page():
    Response("Hi", media_type='text/html')