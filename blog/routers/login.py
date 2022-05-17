from fastapi import APIRouter, Depends, HTTPException,status
from .. import schemas as _schemas, databases, models as _models
from sqlalchemy.orm import Session

router = APIRouter(tags=["User Authentication"])


@router.post("/login")
def login(user_info: _schemas.login, db: Session = Depends(databases.get_db)):
    user = db.query(_models.User.email == user_info.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Username don't exist!"
        )
    return user
