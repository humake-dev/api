from models import Rent, Order, Admin, User
from sqlalchemy.orm import Session
from datetime import datetime

def get_rent_list(db: Session, current_user: User | Admin, skip: int = 0, limit: int = 10):
    _rent_list = db.query(Rent).join(Order).filter(Order.enable == True,Rent.start_datetime < datetime.now(),Rent.end_datetime > datetime.now()).order_by(Order.id.desc())

    if not isinstance(current_user, Admin):
        _rent_list = _rent_list.filter(Order.user_id == current_user.id )

    total = _rent_list.count()
    rent_list = _rent_list.offset(skip).limit(limit).all()
    return total, rent_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_rent(db: Session, current_user: User | Admin, id: int):
    rent = db.query(Rent).get(id)
    return rent