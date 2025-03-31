from datetime import datetime
from models import Exercise
from sqlalchemy.orm import Session

def get_exercise_list(db: Session, session: dict, skip: int = 0, limit: int = 10):
    _exercise_list = db.query(Exercise).order_by(Exercise.id.desc())

    total = _exercise_list.count()
    exercise_list = _exercise_list.offset(skip).limit(limit).all()
    return total, exercise_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_exercise(db: Session, session: dict, exercise_id: int):
    exercise = db.query(Exercise).get(exercise_id)
    return exercise