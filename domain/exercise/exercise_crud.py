from models import Exercise, Admin, User
from sqlalchemy.orm import Session


def get_exercise_list(db: Session, filters: dict = {}, skip: int = 0, limit: int = 10):
    query = db.query(Exercise).join(Exercise.picture,isouter=True)

    # 필터 적용
    for key, value in filters.items():
        query = query.filter(getattr(Exercise, key) == value)

    total = query.count()
    exercise_list = query.order_by(Exercise.id.desc()).offset(skip).limit(limit).all()

    return total, exercise_list


def get_exercise(db: Session, id: int):
    exercise = db.query(Exercise).get(id)
    return exercise