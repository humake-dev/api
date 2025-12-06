from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.admin import admin_schema, admin_crud
from starlette import status
from default_func import *
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

router = APIRouter()


SECRET_KEY =  os.getenv("ENCRYPTED_KEY", "")
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 15
REFRESH_EXPIRE_DAYS = 90

fake_users = {"test@test.com": {"password": "1234", "user_id": 1}}

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/admin_login", response_model=admin_schema.Admin)
def login(response: Response, db: Session = Depends(get_db), admin_id: int = None,form: OAuth2PasswordRequestForm = Depends()):
    admin = admin_crud.get_admin(db, admin_id, form.login_id, form.password)
    #if not user or user["password"] != form.password:
    #    raise HTTPException(400, "Invalid credentials")

    access = create_token({"branch_id": admin.branch_id,"sub": admin.uid}, timedelta(minutes=ACCESS_EXPIRE_MINUTES))
    refresh = create_token({"sub": admin.uid}, timedelta(days=REFRESH_EXPIRE_DAYS))

    return {"access_token": access, "refresh_token": refresh}


#@router.post("/admin_login", response_model=admin_schema.Admin)
#def login(response: Response, db: Session = Depends(get_db), admin_id: int = None, login_id: str = None ,password: str = None):
#    admin = admin_crud.get_admin(db, admin_id, login_id, password)
#
#    session_data = {"admin_id": admin_id, "branch_id": admin.branch_id}
#    session_cookie = serializer.dumps(session_data)

#    response.set_cookie(
#        key=SESSION_COOKIE_NAME,        # PHP와 절대 겹치지 않는 이름
#        value=session_cookie,
#        httponly=True,
#        samesite="Lax",            # PHP 기본과 동일
#    )

#    return admin

@router.post("/admin_logout")
def logout(response: Response):
    response.delete_cookie(SESSION_COOKIE_NAME)
    return {"message": "Logged out"}


@router.post("/refresh")
def refresh(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(401, "Invalid refresh token")

    access = create_token({"sub": username}, timedelta(minutes=ACCESS_EXPIRE_MINUTES))
    return {"access_token": access}