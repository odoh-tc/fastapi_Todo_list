import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import models
from database import engine
from passlib.context import CryptContext
from fastapi import status, HTTPException, Request
from routers.user import logout


load_dotenv()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

models.Base.metadata.create_all(bind=engine)

def verify_password(plain_password, hash_password):
    return bcrypt_context.verify(plain_password, hash_password)

def get_password_hash(password):
    return bcrypt_context.hash(password)



async def get_current_user(request: Request):
    try:
        token = request.cookies.get('access_token')
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            logout(request)
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found")




async def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users)\
        .filter(models.Users.username == username)\
        .first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


def create_access_token(username: str, user_id: int, 
                        expires_delta: Optional[timedelta] = None):
    encode = {'sub': username, 'id': user_id}
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=20)
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)






