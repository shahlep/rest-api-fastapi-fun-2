from fastapi import APIRouter

router = APIRouter(
    tags=['User Authentication']
)


@router.post('/login')
def login():
    pass
