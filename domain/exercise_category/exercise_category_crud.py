from datetime import datetime
from models import ExerciseCategory
from sqlalchemy.orm import Session

def get_exercise_category_list(db: Session, skip: int = 0, limit: int = 10):
    _exercise_category_list = db.query(ExerciseCategory).order_by(ExerciseCategory.id.desc())

    total = _exercise_category_list.count()
    exercise_category_list = _exercise_category_list.offset(skip).limit(limit).all()
    return total, exercise_category_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_exercise_category(db: Session, exercise_category_id: int):
    exercise_category = db.query(ExerciseCategory).get(exercise_category_id)
    return exercise_category