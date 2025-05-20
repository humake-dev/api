from models import Enroll, Order
from sqlalchemy.orm import Session
from datetime import date

def get_enroll_list(db: Session, session: dict, skip: int = 0, limit: int = 10):
    _enroll_list = db.query(Enroll).join(Order).filter(Order.user_id == session['user_id'],Order.enable == True,Enroll.start_date < date.today(),Enroll.end_date > date.today()).order_by(Order.id.desc())

    total = _enroll_list.count()
    enroll_list = _enroll_list.offset(skip).limit(limit).all()
    return total, enroll_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_enroll(db: Session, session: dict, id: int):
    enroll = db.query(Enroll).get(id)
    return enroll