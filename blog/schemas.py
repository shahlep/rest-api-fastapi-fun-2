from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    content: str


# https://pydantic-docs.helpmanual.io/usage/models/#recursive-orm-models
class ShowBlog(Blog):
    class Config:
        orm_mode = True

