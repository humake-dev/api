from datetime import datetime
from models import Entrance
from sqlalchemy import func
from sqlalchemy import extract
from sqlalchemy.orm import Session

def get_entrance_list(db: Session, session: dict, filters: dict = {}, skip: int = 0, limit: int = 10):
    query = db.query(Entrance).filter(Entrance.user_id == session['user_id'])

    for key, value in filters.items():
        if key == 'year' and value:
            query = query.filter(extract('year', Entrance.created_at) == value)
        elif key == 'month' and value:
            query = query.filter(extract('month', Entrance.created_at) == value)
        else:
            query = query.filter(getattr(Entrance, key) == value)

    total = query.group_by(func.date(Entrance.created_at)).count()
    entrance_list = query.order_by(Entrance.id.desc()).offset(skip).limit(limit).all()
    return total, entrance_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_entrance(db: Session, session: dict, id: int):
    entrance = db.query(Entrance).filter(Entrance.user_id == session['user_id'],Entrance.id == id).first()
    return entrance