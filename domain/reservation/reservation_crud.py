from datetime import datetime, timedelta
from models import ReservationUser,Reservation,Trainer, Admin, User
from sqlalchemy import select, func, extract
from sqlalchemy.orm import Session

def get_reservation_list(db: Session, current_user: User | Admin, filters: dict = {}, skip: int = 0, limit: int = 10):
    query = db.query(Reservation).join(ReservationUser).filter(User.branch_id == current_user.branch_id)

    if not isinstance(current_user, Admin):
        query = query.filter(ReservationUser.user_id == current_user.id)

    conditions = [
        ReservationUser.user_id == current_user.id,
        Reservation.enable == True,
        ]

    for key, value in filters.items():
        if key == 'year' and value:
            query = query.filter(extract('year', Reservation.start_time) == value)
        elif key == 'month' and value:
            query = query.filter(extract('month', Reservation.start_time) == value)
        elif key == 'day' and value:
            query = query.filter(extract('day', Reservation.start_time) == value)
        else:
            query = query.filter(getattr(Reservation, key) == value)

    base_stmt: Select = (
        select(Reservation.id, Reservation.start_time, Reservation.end_time, Reservation.enable,
               Reservation.created_at, ReservationUser.user_id, ReservationUser.complete,
               ReservationUser.complete_at, Trainer.name.label("trainer_name"))
        .join(ReservationUser).join(Trainer)
        .where(*conditions)  # ✅ 리스트 풀어서 넘김
    )

    count_stmt = select(func.count()).select_from(base_stmt.subquery())
    total = db.execute(count_stmt).scalar()

    data_stmt = base_stmt.order_by(Reservation.start_time.asc()).offset(skip).limit(limit)
    reservation_list = db.execute(data_stmt).mappings().all()

    return total, reservation_list

def get_reservation(db: Session, current_user: User | Admin, id: int):
    stmt = (
        select(Reservation)
        .join(ReservationUser)
        .where(Reservation.branch_id == current_user.branch_id)
        .where(Reservation.id == id)
    )

    if not isinstance(current_user, Admin):
        stmt = stmt.where(ReservationUser.user_id == current_user.id)

    return db.execute(stmt).scalars().first()