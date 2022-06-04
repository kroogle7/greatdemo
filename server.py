from ast import Delete
from re import template
from typing import Optional
from unicodedata import name
from fastapi import FastAPI, Form, Cookie
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
def index_page(username: Optional[str] = Cookie(default=None)):
    with open('templates/index.html', 'r') as f:
        login_page = f.read()
        if username:
            try:
                user = users[username]
            except KeyError:
                response =  Response(login_page,media_type='text/html')
                response.delete_cookie(key='username')
                return response
            return Response(f"Hello, {users[username]['name']}!",media_type='text/html')
    return Response(login_page, media_type='text/html')

@app.post('/login')
def process_login_page(username: str = Form(...), password: str = Form(...)):
    user = users.get(username)
    if not user or user['password'] != password:
        return Response('This user is not registered',media_type="text/html")

    response =  Response(
        f"Hello, {user['name']}<br /> Balance:{user['balance']}",
        media_type='text/html')
    response.set_cookie(key='username',value=username)
    return response

