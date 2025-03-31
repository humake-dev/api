from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.user import user_schema, user_crud
from starlette import status
from default_func import *

router = APIRouter()

@router.get("/user", response_model=user_schema.User)
def user_detail( db: Session = Depends(get_db),session: dict = Depends(get_session)):
    user = user_crud.get_user(db, session)

    if user is None:
        raise HTTPException(status_code=404, detail="trainer not found")

    return user

@router.post("/login")
def login(response: Response, user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, {"user_id": user_id})

    session_data = {"user_id": user_id, "branch_id": user.branch_id}
    session_cookie = serializer.dumps(session_data)
    response.set_cookie(key=SESSION_COOKIE_NAME, value=session_cookie, httponly=True)
    return {"message": "Session set"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(SESSION_COOKIE_NAME)
    return {"message": "Logged out"}