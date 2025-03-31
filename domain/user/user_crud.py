from models import User
from sqlalchemy.orm import Session


def get_user(db: Session, session: dict):
    user = db.query(User).join(User.user_picture,isouter=True).filter(User.id== session['user_id'], User.enable == True).first()
    return user

def get_user_by_phone(db: Session, phone: str):
    user = db.query(User).filter(User.phone == phone).first()
    return user

def login(user_id: int, password: str):
    user = db.query(User).filter(User.id == user_id).filter(User.phone==password).first()
    return user