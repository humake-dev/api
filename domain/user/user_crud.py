from fastapi import HTTPException, status
from sqlalchemy.orm import Session, aliased
from models import User, UserWeight  # 모델 임포트 예시
from sqlalchemy import func,select



def get_user(
    db: Session,
    user_id: int = None,
    login_id: int = None,
    phone: str = None
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

    elif login_id is not None and phone is not None:
        # login
        user = (
            db.query(User)
            .filter(User.login_id == login_id)
            .filter(User.phone == phone)  # 실제 구현 시엔 비밀번호 해싱 필요
            .first()
        )
        return user

    elif phone:
        user = db.query(User).filter(User.phone == phone).first()
        return user

    else:
        # 아무 것도 없을 경우 에러
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id, (login_id and password), or phone must be provided."
        )
