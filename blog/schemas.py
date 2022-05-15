from pydantic import BaseModel
from typing import List


class BlogBase(BaseModel):
    title: str
    content: str


class Blog(BlogBase):
    class Config:
        orm_mode = True


# https://pydantic-docs.helpmanual.io/usage/models/#recursive-orm-models


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog]

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    content: str
    content_creator: ShowUser

    class Config:
        orm_mode = True
