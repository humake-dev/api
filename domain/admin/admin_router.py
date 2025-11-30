from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.admin import admin_schema, admin_crud
from starlette import status
from default_func import *

router = APIRouter()

@router.post("/admin_login", response_model=admin_schema.Admin)
def login(response: Response, db: Session = Depends(get_db), admin_id: int = None, login_id: int = None ,phone: str = None):
    admin = admin_crud.get_admin(db, admin_id, login_id, phone)

    session_data = {"admin_id": admin_id, "branch_id": admin.branch_id}
    session_cookie = serializer.dumps(session_data)

    response.set_cookie(
        key=SESSION_COOKIE_NAME,        # PHP와 절대 겹치지 않는 이름
        value=session_cookie,
        httponly=True,
        samesite="Lax",            # PHP 기본과 동일
    )

    return admin

@router.post("/admin_logout")
def logout(response: Response):
    response.delete_cookie(SESSION_COOKIE_NAME)
    return {"message": "Logged out"}