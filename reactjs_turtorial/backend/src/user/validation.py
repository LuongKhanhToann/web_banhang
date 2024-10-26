from datetime import datetime, timedelta, timezone
import re
from typing import Union
from fastapi import Depends, HTTPException
from user import models


def check_email_is_unique(email: str, db):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        return False
    return True

def check_email_is_valid(email: str):
    email_validate_pattern = r"^\S+@\S+\.\S+$"
    return re.match(email_validate_pattern, email)

def check_password_is_valid(password: str):
    return len(password) >= 6
    
def check_username_is_valid(username: str):
    return len(username) >= 6
    
def check_phone_number_is_valid(phone_number: str):
    phone_number_validate_pattern = r"^[0-9]{10,11}$"
    re.match(phone_number_validate_pattern, phone_number)
    return re.match(phone_number_validate_pattern, phone_number)

def check_user_id_valid(user_id: int, db):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        return True
    return False
    
# authentication
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from dotenv import load_dotenv
from os import environ

from pydantic import BaseModel

load_dotenv()

SECRET_KEY = environ.get('SECRET_KEY')
ALGORITHM = environ.get('ALGORITHM')

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
    
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        username: str = payload.get("username")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    return {
        "email": email,
        "role": role,
        "username":username
    }