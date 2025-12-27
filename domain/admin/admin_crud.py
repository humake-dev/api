from fastapi import HTTPException, status
from sqlalchemy.orm import Session, aliased
from models import Admin
import bcrypt
import os


def authenticate_admin(db: Session,
    login_id: str = None,
    password: str = None
):
    if login_id is not None and password is not None:
        admin = db.query(Admin).filter(Admin.uid == login_id).first()
        if not admin:
            return None

        if not verify_password(password, admin.encrypted_password):
            return None

        return admin
    else:
        # 아무 것도 없을 경우 에러
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="admin_id, (admin_id and password), or phone must be provided."
        )

def verify_password(password: str, hashed: str) -> bool:
    key = os.getenv("ENCRYPTED_KEY", "")
    raw = (password + key).encode()
    return bcrypt.checkpw(raw, hashed.encode())
