from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.user import user_schema, user_crud
from default_func import *
from typing import List
import re

router = APIRouter(prefix="/users", dependencies=[Depends(get_admin_session)])

@router.get("/", response_model=List[user_schema.User])
def get_users_by_phone(phone: str, db: Session = Depends(get_db), session: dict = Depends(get_admin_session)):
    # 숫자만 남기고 나머지 제거
    cleaned_phone = re.sub(r'[^0-9]', '', phone)

    users = user_crud.get_users(db, session, phone=cleaned_phone)
    if not users:
        raise HTTPException(status_code=404, detail="users not found")
    return users
