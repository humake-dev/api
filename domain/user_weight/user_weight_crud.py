from datetime import datetime
from models import UserWeight
from sqlalchemy import func
from sqlalchemy.orm import Session
from domain.user_weight import user_weight_schema


def get_user_weight_list(db: Session, session: dict, filters: dict = {}, skip: int = 0, limit: int = 10):
    user_id = session['user_id']

    # 기본 필터: 현재 로그인한 유저의 데이터만
    base_query = db.query(
        func.avg(UserWeight.weight).label('avg_weight')
    ).filter(UserWeight.user_id == user_id)

    # 그룹 기준 설정
    if filters.get('month'):
        group_field = func.date_format(UserWeight.created_at, "%Y-%m")  # '2025-05'
    elif filters.get('week'):
        group_field = func.yearweek(UserWeight.created_at)
    else:
        group_field = func.date(UserWeight.created_at)

    # 그룹 기준도 select에 포함
    query = base_query.add_columns(group_field.label('group_date')).group_by(group_field)

    total = query.count()  # 전체 그룹 개수
    user_weight_list = query.order_by(group_field.desc()).offset(skip).limit(limit).all()

    return total, user_weight_list

def set_user_weight(db: Session, session: dict, user_weight_data: user_weight_schema.UserWeightCreate):
    user_weight = UserWeight(
        user_id=session['user_id'],
        weight=user_weight_data.weight
    )
    db.add(user_weight)
    db.commit()

    return user_weight.id