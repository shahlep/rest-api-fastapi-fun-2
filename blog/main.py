from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas as _schemas
from . import models as _models
from .databases import engine, SessionLocal
from sqlalchemy.orm import Session

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


@app.get('/blog', status_code=status.HTTP_200_OK)
def all_blog(db: Session = Depends(get_db)):
    blogs = db.query(_models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
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
