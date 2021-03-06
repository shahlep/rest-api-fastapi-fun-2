from fastapi import APIRouter, status, Depends, HTTPException
from .. import databases, models as _models, schemas as _schemas
from ..hashing import Hash
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/user", tags=["User"])

get_db = databases.get_db


@router.post("/")
def create_user(user: _schemas.User, db: Session = Depends(get_db)):
    new_user = _models.User(
        name=user.name, email=user.email, password=Hash.encrypt(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
    "",
    response_model=_schemas.ShowUser,
    status_code=status.HTTP_200_OK,
)
def get_user_by_name(name: str, db: Session = Depends(get_db)):
    name = db.query(_models.User).filter(_models.User.name == name).first()
    return name


@router.get(
    "/",
    response_model=List[_schemas.ShowUser],
    status_code=status.HTTP_200_OK,
)
def get_all_user(db: Session = Depends(get_db)):
    users = db.query(_models.User).all()
    return users


@router.get(
    "/{id}",
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
