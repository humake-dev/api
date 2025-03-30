from datetime import datetime
from models import User
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int):
    user = db.query(User).get(user_id)
    return user

def get_user_by_phone(db: Session, phone: str):
    user = db.query(User).filter(User.phone == phone).first()
    return user

def login(login_id: str, password: str):
    user = db.query(User).filter(User.id == user_id).filter(User.phone==password).first()
    return user