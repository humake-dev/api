from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from domain.user import user_schema, user_crud
from default_func import *
import re
from typing import Union, List

router = APIRouter(prefix="/users", dependencies=[Depends(get_current_user)])

@router.get("", response_model=Union[user_schema.User, List[user_schema.User]])
def get_user_by_phone(phone: str, db: Session = Depends(get_db), current_user:  Admin = Depends(get_current_user)):
    # 숫자만 남기고 나머지 제거
    cleaned_phone = re.sub(r'[^0-9]', '', phone)

    users = user_crud.get_user_by_phone(db, current_user, phone=cleaned_phone)
    if not users:
        raise HTTPException(status_code=404,
                            detail={
                                "code": "USERS_NOT_FOUND",
                                "message": "users not found"
                            })
    return users
