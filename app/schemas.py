from pydantic import BaseModel,EmailStr
from typing import List, Optional, Union
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str=None
    published: bool=True
    class Config:
        orm_mode = True

class User(BaseModel):
    id:int
    first_name: str
    last_name: str=None
    email_id: EmailStr=None
    class Config:
        orm_mode = True

class Vote(BaseModel):

    post_id:int
    direction:bool
    class Config:
        orm_mode = True

class UpdateItem(Post):
    updated_at: Optional[datetime]=datetime.utcnow()
    class Config:
        orm_mode = True

class ReadItem(Post):
    id:str
    user_id:int
    created_at: Optional[datetime]=datetime.now()
    updated_at: Optional[datetime]=datetime.now()
    user:User
    class Config:
        orm_mode = True

class ReadItemVotes(BaseModel):
    Post:ReadItem
    votes:int

    class Config:
        orm_mode = True


class GetResponseItem(BaseModel):
    message:str
    payload:List[ReadItemVotes]
    class Config:
        orm_mode = True

class CreateResponseItem(BaseModel):

    message:str
    payload:ReadItem

    class Config:
        orm_mode = True

class UpdateResponseItem(BaseModel):

    message:str
    payload:Post

    class Config:
        orm_mode = True

class ReadUserInput(User):
    id:Optional[str]
    password:str
    created_at: Optional[datetime]=datetime.now()
    updated_at: Optional[datetime]=datetime.now()
    class Config:
        orm_mode = True

class ReadUserResponse(User):
    id:str
    created_at: Optional[datetime]=datetime.now()
    updated_at: Optional[datetime]=datetime.now()
    posts:List[Post]
    class Config:
        orm_mode = True

class CreateResponseUser(BaseModel):

    message:str
    payload:ReadUserResponse

    class Config:
        orm_mode = True


class Login(BaseModel):
    username:EmailStr
    password:str