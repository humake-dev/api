from http.client import HTTPException

from models import Entrance, Admin, User
from sqlalchemy import func
from sqlalchemy import extract
from sqlalchemy.orm import Session
from datetime import datetime

def get_entrance_list(db: Session, current_user: User | Admin, filters: dict = {}, skip: int = 0, limit: int = 10):
    query = db.query(Entrance).join(Entrance.user).filter(User.branch_id == current_user.branch_id)

    if not isinstance(current_user, Admin):
        query = query.filter(Entrance.user_id == current_user.id)

    has_day_filter = False

    for key, value in filters.items():
        if key == 'year' and value:
            query = query.filter(extract('year', Entrance.in_time) == value)
        elif key == 'month' and value:
            query = query.filter(extract('month', Entrance.in_time) == value)
        elif key == 'day' and value:
            has_day_filter = True
            query = query.filter(extract('day', Entrance.in_time) == value)
        else:
            query = query.filter(getattr(Entrance, key) == value)

    if has_day_filter:
        total = query.count()
    else:
        total = query.group_by(func.date(Entrance.in_time)).count()

    # entrance_list 분기
    if has_day_filter:
        entrance_list = (
            query
            .order_by(Entrance.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    else:
        entrance_list = (
            query
            .group_by(func.date(Entrance.in_time))
            .order_by(Entrance.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    return total, entrance_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_entrance(db: Session, current_user: User | Admin, id: int):
    if isinstance(current_user, Admin):
        entrance = db.query(Entrance).filter(Entrance.branch_id == current_user.branch_id ,Entrance.id == id).first()
    else:
        entrance = db.query(Entrance).filter(Entrance.user_id == current_user.id ,Entrance.id == id).first()

    return entrance

def set_entrance(db: Session,  user_id: int):
    now = datetime.now().replace(microsecond=0)
    entrance = Entrance(
        user_id=user_id,
        in_time=now,
        created_at=now
    )
    db.add(entrance)
    db.commit()

    return entrance.id
