from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas as _schemas, databases, models as _models, jwttoken
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(tags=["User Authentication"])


@router.post("/login")
def login(user_info: _schemas.User, db: Session = Depends(databases.get_db)):
    user = (
        db.query(_models.User).filter(_models.User.email == user_info.email).first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Username don't exist!"
        )
    if not Hash.verify(user.password, user_info.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid password!"
        )
    # return user
    access_token = jwttoken.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
