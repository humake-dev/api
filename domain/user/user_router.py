from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.orm import Session
from domain.user import user_schema, user_crud
from starlette import status
from default_func import *
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

router = APIRouter()

@router.get("/user", response_model=user_schema.User)
def user_detail(
    db: Session = Depends(get_db),
    current_user: User | Admin = Depends(get_current_user),
    user_id: int | None = None,
):
    # user_id로 다른 유저 조회 시도
    if user_id is not None:
        # admin만 허용
        if not isinstance(current_user, Admin):
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        user = user_crud.get_user(db, user_id=user_id)

    # 자기 자신 조회
    else:
        user = current_user

    if user is None:
        raise HTTPException(status_code=404,
            detail={
                "code": "USERS_NOT_FOUND",
                "message": "users not found"
            })

    return user

@router.post("/login", response_model=user_schema.TokenResponse)
def login(db: Session = Depends(get_db), form: OAuth2PasswordRequestForm = Depends()):

    # username = "branch_id#user_id"
    try:
        branch_str, user_str = form.username.split("#")
        branch_id = int(branch_str)
        user_id = int(user_str)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid username format. Use branch_id#user_id"
        )

    user = user_crud.get_user_by_branch_user_phone(
        db=db,
        branch_id=branch_id,
        user_id=user_id,
        password=form.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access = create_token(
        {"sub": str(user.id), "role": "user"},
        timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    )

    refresh = create_token(
        {"sub": str(user.id), "role": "user"},
        timedelta(days=REFRESH_EXPIRE_DAYS)
    )

    return {
        "access_token": access,
        "refresh_token": refresh
    }

@router.post("/logout")
def logout(
    payload: user_schema.LogoutRequest,
    db: Session = Depends(get_db),
):
    refresh_token = payload.refresh_token
    return {"message": "logged out"}
