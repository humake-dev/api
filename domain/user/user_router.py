from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.user import user_schema, user_crud
from starlette import status
from default_func import get_current_user

router = APIRouter()

@router.get("/user", response_model=user_schema.User, dependencies=[Depends(get_current_user)])
def user_detail( db: Session = Depends(get_db),user_id: int = Depends(get_current_user)):
    user = user_crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="trainer not found")

    return user

@router.post("/login")
async def login(request: Request):
    request.session["user_id"] = 11632  # 세션에 저장
    return {"message": "로그인 성공"}

@router.post("/logout")
async def logout(request: Request, response: Response):
    request.session.clear()  # 세션 삭제
    return {"message": "로그아웃 성공"}