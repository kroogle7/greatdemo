from typing import Optional

import base64
import hmac
import hashlib

from fastapi import FastAPI, Form, Cookie
from fastapi.responses import Response

app = FastAPI()


SECRET_KEY = "8f1f127477ce3681e45dfb5cbd197cb7aa917dd03d4647c39541f861ce223677"

def sign_data(data:str) ->str:
    '''Возвращает подписанные данные data'''
    return hmac.new(
        SECRET_KEY.encode(),
        msg =data.encode(),
        digestmod = hashlib.sha256
        ).hexdigest().upper()

def get_username_from_signed_string(username_signed:str) -> Optional[str]:
    username_base64 , sign = username_signed.split('.')
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username

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
             return Response(login_page, media_type='text/html')
        valid_username = get_username_from_signed_string(username)
        if not valid_username:
            response =  Response(f"Hello, {users[username]['name']}!",media_type='text/html')
            response.delete_cookie(key='username')
            return response


        try:
            user = users[valid_username]
        except KeyError:
            response =  Response(login_page,media_type='text/html')
            response.delete_cookie(key='username')
            return response
        return Response(f"Hello, {users[valid_username]['name']}!",media_type='text/html')


@app.post('/login')
def process_login_page(username: str = Form(...), password: str = Form(...)):
    user = users.get(username)
    if not user or user['password'] != password:
        return Response('This user is not registered',media_type="text/html")

    response =  Response(
        f"Hello, {user['name']}<br /> Balance:{user['balance']}",
        media_type='text/html')

    username_signed = base64.b64encode(username.encode()).decode()+ '.' + \
        sign_data(username)    
    response.set_cookie(key='username',value=username_signed)
    return response

