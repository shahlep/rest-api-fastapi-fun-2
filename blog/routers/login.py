from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .. import schemas as _schemas, databases, models as _models
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..jwttoken import *
from datetime import datetime, timedelta

router = APIRouter(tags=["User Authentication"])


@router.post("/login")
def login(user_info: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(databases.get_db)):
    user = (
        db.query(_models.User).filter(_models.User.email == user_info.username).first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Username don't exist!"
        )
    if not Hash.verify(user_info.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid password!"
        )
    # return user
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
