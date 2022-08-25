from typing import List, Union

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    post: str


class CreatePost(PostBase):
    pass


class Post(PostBase):
    id: int
    author_id: int


    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    posts: List[Post] = []

    class config:
        orm_mode = True

class Votes(BaseModel):
    post_id: int

class Follower(BaseModel):
    following_id: int