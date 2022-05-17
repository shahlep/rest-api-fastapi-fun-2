from fastapi import APIRouter
from .. import schemas as _schemas

router = APIRouter(
    tags=['User Authentication']
)


@router.post('/login')
def login(user_info: _schemas.login):
    pass
