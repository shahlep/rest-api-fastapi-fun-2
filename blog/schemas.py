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


class ShowUserBase(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    content: str
    content_creator: ShowUserBase

    class Config:
        orm_mode = True


class ShowUser(ShowUserBase):
    name: str
    email: str
    blogs: List[Blog]

    class Config:
        orm_mode = True
