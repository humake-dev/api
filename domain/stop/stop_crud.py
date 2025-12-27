from models import Stop, Admin, User
from sqlalchemy.orm import Session
from domain.stop import stop_schema

def get_stop_list(db: Session, current_user: User, skip: int = 0, limit: int = 10):
    _stop_list = db.query(Stop).filter(Stop.user_id == current_user.id).order_by(Stop.id.desc())

    total = _stop_list.count()
    stop_list = _stop_list.offset(skip).limit(limit).all()
    return total, stop_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_stop(db: Session, current_user: User, id: int):
    stop = db.query(Stop).get(id)
    return stop

def set_stop(db: Session, current_user: User, stop_data: stop_schema.StopCreate):
    stop = Stop(
        user_id=current_user.id,
        stop_start_date=stop_data.stop_start_date,
        stop_end_date=stop_data.stop_end_date,
        description=stop_data.description
    )
    db.add(stop)
    db.commit()
    db.refresh(stop)

    return stop.id