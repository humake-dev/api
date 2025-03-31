from datetime import datetime
from models import ReservationUser,Reservation
from sqlalchemy.orm import Session

def get_reservation_list(db: Session, session: dict, skip: int = 0, limit: int = 10):
    _reservation_list = db.query(ReservationUser).join(Reservation).filter(ReservationUser.user_id == session['user_id']).order_by(Reservation.id.desc())

    total = _reservation_list.count()
    reservation_list = _reservation_list.offset(skip).limit(limit).all()
    return total, reservation_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_reservation(db: Session, session: dict, reservation_id: int):
    reservation = db.query(ReservationUser).join(Reservation).filter(ReservationUser.user_id == session['user_id']).filter(Reservation.id == reservation_id).first()
    return reservation