from datetime import datetime
from models import Entrance
from sqlalchemy.orm import Session

def get_entrance_list(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    _entrance_list = db.query(Entrance).filter(Entrance.user_id == user_id).order_by(Entrance.id.desc())

    total = _entrance_list.count()
    entrance_list = _entrance_list.offset(skip).limit(limit).all()
    return total, entrance_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_entrance(db: Session, user_id: int, entrance_id: int):
    entrance = db.query(Entrance).filter(Entrance.user_id == user_id, Entrance.id == entrance_id).first()
    return entrance