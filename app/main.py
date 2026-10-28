from fastapi import Depends, FastAPI, HTTPException,status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from app.oauth2 import create_access_token, get_current_user
from .database import engine,get_db
from . import models, vote, database, oauth2
from . import schemas
from sqlalchemy import func

import asyncio

# models.Base.metadata.create_all(bind= engine)

class Data(BaseModel):
    name:str

origins = ["*"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(vote.router)
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")




@app.get("/")
def root():

    return{"server":"server"}

@app.post("/product")
def post_create(post:Data,db:Session = Depends(get_db)):
    new_post = models.User(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@app.post('/login')
def login_user(user_credential:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credential")
    access_token = create_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}

@app.get("/moon",response_model=list[schemas.Posts])
def test_auth(user:dict = Depends(get_current_user),db:Session = Depends(get_db),limit:int=10):
    posts = db.query(models.Post).limit(limit).all()
    return posts
@app.get("/posts")
def get_posts(db:Session = Depends(database.get_db),current_user:int = Depends(oauth2.get_current_user)):
    result = db.query(models.Post)

    return result
