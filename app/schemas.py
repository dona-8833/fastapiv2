from datetime import datetime
from pydantic import BaseModel,conint


class User(BaseModel):
    name:str
    id:int

class Token(BaseModel):
    access_token:str
    token_type:str
class Posts(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime
    owner: User

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)

