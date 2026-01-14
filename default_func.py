from fastapi import  Request, Depends, HTTPException
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime, timedelta, timezone
from models import Admin,User

SECRET_KEY = os.getenv(
    "ENCRYPTED_KEY",
    "awerigkpawegikp23k1233sdaglpaw!@E$a"  # 개발용 fallback
)
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 15
REFRESH_EXPIRE_DAYS = 90

ROLE_LEVEL = {
    "user": 1,
    "admin": 2,
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": int(expire.timestamp())})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "sub" not in payload or "role" not in payload:
            raise HTTPException(401, "Invalid token payload")
        return payload
    except JWTError:
        raise HTTPException(401, "Invalid token")


def require_role(min_role: str):
    def checker(payload: dict = Depends(get_current_payload)):
        role = payload.get("role")
        if role not in ROLE_LEVEL:
            raise HTTPException(403, "Invalid role")

        if ROLE_LEVEL[role] < ROLE_LEVEL[min_role]:
            raise HTTPException(403, "Permission denied")

        return payload
    return checker

def get_current_user(
    payload: dict = Depends(require_role("user")),
    db: Session = Depends(get_db)
):
    role = payload["role"]
    user_id = payload["sub"]

    if role == "admin":
        entity = db.query(Admin).get(user_id)
    else:
        entity = db.query(User).get(user_id)

    if not entity:
        raise HTTPException(404, "Account not found")

    return entity
