from datetime import timedelta,datetime

import jwt
from fastapi import Depends,HTTPException,status
from jose.exceptions import JWEError
from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from app import models
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
"johndoe": {
"username": "johndoe",
"password": pwd_context.hash("password123"),
# Hashed password
}
}

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_user(db,username:str):
    if username in db:
        return db[username]
    return None
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
def verify_access_token(token,credential_exception):
    try:
        token_data = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = token_data.get("user_id")
        if user_id is None:
            raise credential_exception
    except JWEError:
        raise credential_exception
    return user_id
def get_current_user(token:str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credential",headers={"WWW-authenticate":"Bearer"})
    token_data = verify_access_token(token,credential_exception)
    user = db.query(models.User).filter(models.User.id == token_data).first()
    return user
