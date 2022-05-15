from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas as _schemas
from . import models as _models
from .hashing import Hash
from .databases import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

_models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(blog: _schemas.Blog, db: Session = Depends(get_db)):
    new_blog = _models.Blog(title=blog.title, content=blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[_schemas.ShowBlog], status_code=status.HTTP_200_OK)
def all_blog(db: Session = Depends(get_db)):
    blogs = db.query(_models.Blog).all()
    return blogs


@app.get('/blog/{id}', response_model=_schemas.ShowBlog, status_code=status.HTTP_200_OK)
def get_blog_by_id(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(_models.Blog).filter(_models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
    return blog


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog_by_id(id, blog_org: _schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(_models.Blog).filter(_models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')
    blog.update(blog_org)
    db.commit()
    return 'Updated'


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog_by_id(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(_models.Blog).filter(_models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'delete task done'


@app.post('/user')
def create_user(user: _schemas.User, db: Session = Depends(get_db)):
    new_user = _models.User(name=user.name, email=user.email, password=Hash.encrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user', response_model=List[_schemas.ShowUser], status_code=status.HTTP_200_OK)
def all_User(db: Session = Depends(get_db)):
    users = db.query(_models.User).all()
    return users


@app.get('/user/{id}', response_model=_schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_user_by_id(id, response: Response, db: Session = Depends(get_db)):
    user = db.query(_models.User).filter(_models.User.id == id).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
    return user
