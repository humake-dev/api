from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.user import user_schema, user_crud
from starlette import status
from default_func import *

router = APIRouter()

@router.get("/user", response_model=user_schema.User)
def user_detail( db: Session = Depends(get_db),session: dict = Depends(get_session), user_id: int = None):
    admin_id = session.get('admin_id')

    if admin_id:
        user = user_crud.get_user(db, user_id=user_id)
    else: 
        user_id = session.get('user_id')
        if user_id:
            user = user_crud.get_user(db, user_id=user_id)
        else:
            user = user_crud.get_user(db, session)        
            
    if user is None:
        raise HTTPException(status_code=404, detail="trainer not found")

    return user

@router.post("/login", response_model=user_schema.User)
def login(response: Response, db: Session = Depends(get_db), user_id: int = None, login_id: int = None ,phone: str = None):
    user = user_crud.get_user(db, user_id, login_id, phone)

    session_data = {"user_id": user.id, "branch_id": user.branch_id}
    session_cookie = serializer.dumps(session_data)

    response.set_cookie(
        key=SESSION_COOKIE_NAME,        # PHP와 절대 겹치지 않는 이름
        value=session_cookie,
        httponly=True,
        samesite="Lax",            # PHP 기본과 동일
    )

    return user

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(SESSION_COOKIE_NAME)
    return {"message": "Logged out"}