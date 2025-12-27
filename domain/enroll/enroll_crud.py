from models import Enroll, Order, Admin, User
from sqlalchemy.orm import Session
from datetime import date

def get_enroll_list(db: Session, current_user: User | Admin, skip: int = 0, limit: int = 10, user_id: int | None = None):
    _enroll_list = db.query(Enroll).join(Order).filter(Order.branch_id == current_user.branch_id, Order.enable == True,Enroll.start_date < date.today(),Enroll.end_date > date.today()).order_by(Order.id.desc())

    if isinstance(current_user, Admin):
        _enroll_list = _enroll_list.filter(Order.user_id == user_id )
    else:
        _enroll_list = _enroll_list.filter(Order.user_id == current_user.id )


    total = _enroll_list.count()
    enroll_list = _enroll_list.offset(skip).limit(limit).all()
    return total, enroll_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_enroll(db: Session, current_user: User | Admin, id: int):
    enroll = db.query(Enroll).get(id)
    return enroll