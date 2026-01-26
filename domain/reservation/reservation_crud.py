from datetime import datetime, timedelta
from models import ReservationUser,Reservation,Trainer, Admin, User
from sqlalchemy import select, func, extract
from sqlalchemy.orm import Session

from sqlalchemy import select, func, extract
from sqlalchemy.orm import Session

def get_reservation_list(
    db: Session,
    current_user: User | Admin,
    filters: dict | None = None,
    skip: int = 0,
    limit: int = 10,
):
    filters = filters or []

    conditions = [
        Reservation.enable.is_(True),
        User.branch_id == current_user.branch_id,
    ]

    # 일반 유저면 본인 예약만
    if not isinstance(current_user, Admin):
        conditions.append(ReservationUser.user_id == current_user.id)

    # 날짜 필터
    for key, value in filters.items():
        if not value:
            continue

        if key == "year":
            conditions.append(extract("year", Reservation.start_time) == value)
        elif key == "month":
            conditions.append(extract("month", Reservation.start_time) == value)
        elif key == "day":
            conditions.append(extract("day", Reservation.start_time) == value)
        else:
            conditions.append(getattr(Reservation, key) == value)

    # ✅ 공통 base_stmt
    base_stmt = (
        select(
            Reservation.id,
            Reservation.start_time,
            Reservation.end_time,
            Reservation.enable,
            Reservation.created_at,
            ReservationUser.user_id,
            ReservationUser.complete,
            ReservationUser.complete_at,
            Trainer.name.label("trainer_name"),
        )
        .join(ReservationUser, ReservationUser.reservation_id == Reservation.id)
        .join(User, User.id == ReservationUser.user_id)
        .join(Trainer, Trainer.id == Reservation.manager_id)
        .where(*conditions)
    )

    # 전체 개수
    count_stmt = select(func.count()).select_from(base_stmt.subquery())
    total = db.execute(count_stmt).scalar_one()

    # 페이지 데이터
    data_stmt = (
        base_stmt
        .order_by(Reservation.start_time.asc())
        .offset(skip)
        .limit(limit)
    )

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