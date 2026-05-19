from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
from requests import Session

from storage.database import create_user, get_user_by_username
import os

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")

pwd_context = CryptContext(schemes=['bcrypt'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_token(user_id: int) -> str:

    payload = {'sub': str(user_id), 'exp': datetime.now() + timedelta(minutes=30)}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code = 401)
    return int(user_id)

@router.post("/auth/register")
def register_user(username: str = Form(), password: str = Form()):
    if get_user_by_username(username):
        raise HTTPException(status_code=400, detail="Username already exists")
    hash = pwd_context.hash(password)
    user = create_user(username, hash)
    return {'access_token': create_token(user['id'])}

@router.post("/auth/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not pwd_context.verify(form_data.password, user['password']):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {'access_token': create_token(user['id'])}