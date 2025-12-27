from fastapi import HTTPException, status
from sqlalchemy.orm import Session, aliased
from models import Admin, User, UserWeight  # 모델 임포트 예시
import re

def get_user(
    db: Session,
    user_id: int = None
):

    if user_id:
        # 기존 get_user
        user = (
            db.query(User)
            .join(User.access_card, isouter=True)
            .join(User.picture, isouter=True)
            .join(User.user_trainer, isouter=True)
            .join(User.user_height, isouter=True)
            .join(User.user_weight, isouter=True)
            .filter(User.id == user_id, User.enable == True)
            .first()
        )
        return user

    # 아무 것도 없을 경우 에러
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="user_id, (login_id and password), or phone must be provided."
    )


def get_user_by_phone(
    db: Session,
    password: str = None
):

    if password:
        user = db.query(User).filter(User.phone == re.sub(r"\D", "", password)).first()
        return user

    else:
        # 아무 것도 없을 경우 에러
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id, (login_id and password), or phone must be provided."
        )

def get_user_py_phone(db: Session, current_user: Admin, phone: str):
    try:
        branch_id = current_user.branch_id
        if branch_id is None:
            raise HTTPException(status_code=400, detail="branch_id not found in session")
        return db.query(User).filter(User.branch_id == branch_id, User.phone==phone).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

def get_users_py_phone(db: Session, current_user: Admin, phone: str):
    try:
        branch_id = current_user.branch_id
        if branch_id is None:
            raise HTTPException(status_code=400, detail="branch_id not found in session")
        return db.query(User).filter(User.branch_id == branch_id, User.phone.like(f"%{phone}%")).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")