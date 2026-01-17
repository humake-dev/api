from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.orm import Session
from domain.admin import admin_schema, admin_crud
from starlette import status
from default_func import *
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

router = APIRouter()

@router.post("/admin_login", response_model=admin_schema.TokenResponse)
def login( db: Session = Depends(get_db), form: OAuth2PasswordRequestForm = Depends()):
    admin = admin_crud.authenticate_admin(db, form.username, form.password)
    if not admin:
        raise HTTPException(
            status_code=401,
            detail={
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid credentials"
            }
        )

    access = create_token({"sub": str(admin.id),"role": "admin"}, timedelta(minutes=ACCESS_EXPIRE_MINUTES))
    refresh = create_token({"sub": str(admin.id),"role": "admin"}, timedelta(days=REFRESH_EXPIRE_DAYS))

    return {"access_token": access, "refresh_token": refresh, "branch_id": admin.branch_id}


@router.post("/refresh")
def refresh(data: admin_schema.RefreshTokenRequest):
    try:
        payload = jwt.decode(
            data.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user = payload.get("sub")
        role = payload.get("role")

        if not user or not role:
            raise HTTPException(401, "Invalid refresh token")

    except JWTError:
        raise HTTPException(401, "Invalid refresh token")

    # 🔑 login과 동일한 payload 구조로 access 재발급
    access = create_token(
        {
            "sub": user,
            "role": role
        },
        timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    )

    return {"access_token": access}
