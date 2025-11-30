from fastapi import HTTPException, status
from sqlalchemy.orm import Session, aliased
from models import Admin


def get_admin(
    db: Session,
    admin_id: int = None,
    login_id: int = None,
    phone: str = None
):

    if admin_id:
        # 기존 get_user
        admin = (
            db.query(Admin)
            .join(Admin.picture, isouter=True)
            .filter(Admin.id == admin_id, Admin.enable == True)
            .first()
        )
        return admin

    elif login_id is not None and phone is not None:
        # login
        admin = (
            db.query(Admin)
            .filter(Admin.login_id == login_id)
            .filter(Admin.phone == phone)  # 실제 구현 시엔 비밀번호 해싱 필요
            .first()
        )
        return admin

    else:
        # 아무 것도 없을 경우 에러
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="admin_id, (admin_id and password), or phone must be provided."
        )
