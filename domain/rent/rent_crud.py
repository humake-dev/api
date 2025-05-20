from models import Rent, Order
from sqlalchemy.orm import Session
from datetime import datetime

def get_rent_list(db: Session, session: dict, skip: int = 0, limit: int = 10):
    _rent_list = db.query(Rent).join(Order).filter(Order.user_id == session['user_id'],Order.enable == True,Rent.start_datetime < datetime.now(),Rent.end_datetime > datetime.now()).order_by(Order.id.desc())

    total = _rent_list.count()
    rent_list = _rent_list.offset(skip).limit(limit).all()
    return total, rent_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_rent(db: Session, session: dict, id: int):
    rent = db.query(Rent).get(id)
    return rent