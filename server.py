from re import template
from fastapi import FastAPI, Form
from fastapi.responses import Response

app = FastAPI()

users = {
    "kirill@user.com":{
        "name": "Kirill",
        "password": "some_password1",
        "balance": 500_000
    },
    "dasha@user.com":{
        "name": "Dasha",
        "password": "some_password2",
        "balance": 200_000
    }
}



@app.get("/")
def index_page():
    with open('templates/index.html', 'r') as f:
        login_page = f.read()
    return Response(login_page, media_type='text/html')

@app.post('/login')
def process_login_page(username: str = Form(...), password: str = Form(...)):
    user = users.get(username)
    if not user or user['password'] != password:
        return Response('This user is not registered',media_type="text/html")

    return Response(
    f"Hello, {user['name']}<br /> Balance:{user['balance']}",
    media_type='text/html')
