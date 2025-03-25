from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.user import user_schema, user_crud
from starlette import status

router = APIRouter(
    prefix="/api/user",
)

@router.get("/detail/{user_id}", response_model=user_schema.User)
def user_detail(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id=user_id)
    return user
