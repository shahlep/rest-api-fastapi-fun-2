from fastapi import APIRouter, status, Depends
from .. import databases, models as _models, schemas as _schemas
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

get_db = databases.get_db()


@router.get(
    "/blog",
    tags=["Blog"],
    response_model=List[_schemas.ShowBlog],
    status_code=status.HTTP_200_OK,
)
def all_blog(db: Session = Depends(get_db)):
    blogs = db.query(_models.Blog).all()
    return blogs
