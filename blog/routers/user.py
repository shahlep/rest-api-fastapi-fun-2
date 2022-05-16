from fastapi import APIRouter, status, Depends, HTTPException
from .. import databases, models as _models, schemas as _schemas
from ..hashing import Hash
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

get_db = databases.get_db()


@router.post("/user", tags=["User"])
def create_user(user: _schemas.User, db: Session = Depends(get_db)):
    new_user = _models.User(
        name=user.name, email=user.email, password=Hash.encrypt(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
    "/user",
    tags=["User"],
    response_model=List[_schemas.ShowUser],
    status_code=status.HTTP_200_OK,
)
def all_User(db: Session = Depends(get_db)):
    users = db.query(_models.User).all()
    return users


@router.get(
    "/user/{id}",
    tags=["User"],
    response_model=_schemas.ShowUser,
    status_code=status.HTTP_200_OK,
)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(_models.User).filter(_models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    return user
