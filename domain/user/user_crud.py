from fastapi import HTTPException, status
from sqlalchemy.orm import Session, aliased
from models import Admin, User, UserTrainer, Trainer
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
            .join(UserTrainer.trainer, isouter=True)
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
    """
    - phone 길이가 8이면 정확히 검색
    - phone 길이가 4 이상이면 LIKE 검색, 결과 1개면 반환
    """
    try:
        branch_id = current_user.branch_id
        if branch_id is None:
            raise HTTPException(status_code=400, detail="branch_id not found in session")

        query = db.query(User).filter(User.branch_id == branch_id)

        if len(phone) == 8:
            # 8자리 입력이면 정확히 검색
            user = query.filter(User.phone == phone).first()
            return user

        if len(phone) == 4:
            users = query.filter(User.phone.like(f"%{phone}")).all()
            if len(users) == 1:
                return users[0]
            else:
                # 4자리 이상이면 LIKE 검색
                users = query.filter(User.phone.like(f"%{phone}%")).all()
                if len(users) == 1:
                    return users[0]  # 결과가 1개면 반환
                else:
                    return users  # 결과가 여러 개면 그대로 반환
        elif len(phone) > 4:
            # 4자리 이상이면 LIKE 검색
            users = query.filter(User.phone.like(f"%{phone}%")).all()
            if len(users) == 1:
                return users[0]  # 결과가 1개면 반환
            else:
                return users  # 결과가 여러 개면 그대로 반환
        else:
            return None  # 4자리 미만은 검색하지 않음
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