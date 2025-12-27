from datetime import datetime
from models import UserWeight, Admin, User
from sqlalchemy import func, cast, String, literal
from sqlalchemy.orm import Session
from domain.user_weight import user_weight_schema

def get_user_weight_list(db: Session, current_user: User | Admin, filters: dict = {}, skip: int = 0, limit: int = 10):
    user_id = current_user.id

    # 기본 필터: 현재 로그인한 유저의 데이터만
    base_query = db.query(
        func.round(func.avg(UserWeight.weight), 1).label('avg_weight')
    ).filter(UserWeight.user_id == user_id)

    # 그룹 기준 설정 (항상 string으로 캐스팅)
    if filters.get('month'):
        raw_group_field = func.date_format(UserWeight.created_at, "%Y-%m")  # e.g. '2025-05'
    elif filters.get('week'):
        year_part = func.year(UserWeight.created_at)
        week_part = func.lpad(func.week(UserWeight.created_at, 1), 2, '0')  # ISO week
        raw_group_field = func.concat(
            cast(year_part, String),
            literal('-'),
            week_part)
    else:
        raw_group_field = func.date(UserWeight.created_at)                  # e.g. 2025-05-26 (date)

    group_field = cast(raw_group_field, String)

    # 그룹 기준도 select에 포함
    query = base_query.add_columns(group_field.label('group_date')).group_by(group_field)

    total = query.count()  # 전체 그룹 개수
    user_weight_list = query.order_by(group_field.desc()).offset(skip).limit(limit).all()

    return total, user_weight_list

def set_user_weight(db: Session, current_user: User | Admin, user_weight_data: user_weight_schema.UserWeightCreate):
    user_weight = UserWeight(
        user_id=current_user.id,
        weight=user_weight_data.weight
    )
    db.add(user_weight)
    db.commit()

    return user_weight.id