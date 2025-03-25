from datetime import datetime
from models import User
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int):
    user = db.query(User).get(user_id)
    return user