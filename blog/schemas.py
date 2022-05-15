from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    content: str


# https://pydantic-docs.helpmanual.io/usage/models/#recursive-orm-models
class ShowBlog(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
