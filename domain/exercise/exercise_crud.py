from datetime import datetime
from models import Exercise
from sqlalchemy.orm import Session
from typing import Optional


def get_exercise_list(db: Session, session: dict, filters: dict = {}, skip: int = 0, limit: int = 10):
    query = db.query(Exercise).join(Exercise.picture,isouter=True)

    # 필터 적용
    for key, value in filters.items():
        query = query.filter(getattr(Exercise, key) == value)

    total = query.count()
    exercise_list = query.order_by(Exercise.id.desc()).offset(skip).limit(limit).all()

    return total, exercise_list


def get_exercise(db: Session, session: dict, id: int):
    exercise = db.query(Exercise).get(id)
    return exercise