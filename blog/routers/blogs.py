from fastapi import APIRouter, status, Depends, HTTPException
from .. import databases, models as _models, schemas as _schemas
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

# https://stackoverflow.com/questions/12074726/typeerror-generator-object-is-not-callable
get_db = databases.get_db


@router.get("/blog", tags=["Blog"], response_model=List[_schemas.ShowBlog],
            status_code=status.HTTP_200_OK)
def all_blog(db: Session = Depends(get_db)):
    blogs = db.query(_models.Blog).all()
    return blogs


@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blog"])
def create(blog: _schemas.Blog, db: Session = Depends(get_db)):
    new_blog = _models.Blog(
        title=blog.title, content=blog.content, user_id=blog.user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get(
    "/blog/{id}",
    tags=["Blog"],
    response_model=_schemas.ShowBlog,
    status_code=status.HTTP_200_OK,
)
def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(_models.Blog).filter(_models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    return blog


@router.put("/blog/{id}", tags=["Blog"], status_code=status.HTTP_202_ACCEPTED)
def update_blog_by_id(id: int, blog_org: _schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(_models.Blog).filter(_models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )
    blog.update(blog_org)
    db.commit()
    return "Updated"


@router.delete("/blog/{id}", tags=["Blog"], status_code=status.HTTP_204_NO_CONTENT)
def delete_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(_models.Blog).filter(_models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return "delete task done"
