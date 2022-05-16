from fastapi import FastAPI
from . import models as _models
from .databases import *
from .routers import blog, user

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)

_models.Base.metadata.create_all(bind=engine)

