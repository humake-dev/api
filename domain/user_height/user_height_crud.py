from datetime import datetime
from models import UserHeight
from sqlalchemy import func
from sqlalchemy.orm import Session
from domain.user_height import user_height_schema
from sqlalchemy.dialects.mysql import insert as mysql_insert

def get_user_height(db: Session, session: dict):
    user_height = db.query(UserHeight).filter(UserHeight.user_id == session['user_id']).first()
    return user_height

def set_user_height(db: Session, session: dict, user_height_data: user_height_schema.UserHeightCreate):
    stmt = mysql_insert(UserHeight).values(
        user_id=session['user_id'],
        height=user_height_data.height
    )

    # user_id 충돌 시 height만 업데이트
    on_duplicate_stmt = stmt.on_duplicate_key_update(
        height=stmt.inserted.height
    )

    result = db.execute(on_duplicate_stmt)
    db.commit()

    # 새로 insert된 경우 or 업데이트된 경우의 id 가져오기
    # 삽입된 row의 primary key(id)는 필요시 다음과 같이 가져올 수 있음
    return result.lastrowid