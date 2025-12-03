from fastapi import HTTPException, status
from sqlalchemy.orm import Session, aliased
from models import Admin
import bcrypt
import os

def get_admin(
    db: Session,
    admin_id: int = None,
    login_id: str = None,
    password: str = None
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

    elif login_id is not None and password is not None:

        encrypted=encrypt_password(password)
        # login
        admin = (
            db.query(Admin)
            .filter(Admin.uid == login_id)
            .filter(Admin.encrypted_password == encrypted)  # 실제 구현 시엔 비밀번호 해싱 필요
            .first()
        )
        return admin

    else:
        # 아무 것도 없을 경우 에러
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="admin_id, (admin_id and password), or phone must be provided."
        )




def encrypt_password(password: str):
    key = os.getenv("ENCRYPTED_KEY", "")
    raw = (password + key).encode("utf-8")
    # PHP에서 사용한 salt: '$2a$10$5765dcdeee11439aab5ebO'
    salt = b"$2a$10$5765dcdeee11439aab5ebO"
    encrypted = bcrypt.hashpw(raw, salt)
    return encrypted.decode("utf-8")