from datetime import datetime
from models import UserWeight
from sqlalchemy import func
from sqlalchemy.orm import Session
from domain.user_weight import user_weight_schema

def get_user_weight_list(db: Session, session: dict, filters: dict = {}, skip: int = 0, limit: int = 10):
    query = db.query(UserWeight).filter(UserWeight.user_id == session['user_id'])

    for key, value in filters.items():
        if key == 'month' and value:
            query = query.group_by(func.month(UserWeight.created_at))
        elif key == 'week' and value:
            query = query.group_by(func.week(UserWeight.created_at))
        else:
            query = query.group_by(UserWeight.created_at)

    total = query.count()
    user_weight_list = query.order_by(UserWeight.id.desc()).offset(skip).limit(limit).all()
    return total, user_weight_list  # (전체 건수, 페이징 적용된 질문 목록)

def set_user_weight(db: Session, session: dict, user_weight_data: user_weight_schema.UserWeightCreate):
    user_weight = UserWeight(
        user_id=session['user_id'],
        weight=user_weight_data.weight
    )
    db.add(user_weight)
    db.commit()

    return user_weight.id