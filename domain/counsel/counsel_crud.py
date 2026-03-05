from datetime import datetime
from models import Counsel, CounselContent, CounselUser, Admin, User, CounselResponse
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func
from domain.counsel import counsel_schema


def get_counsel_list(db: Session, current_user: User | Admin, skip: int = 0, limit: int = 10):

    base_stmt = (
        select(
            *Counsel.__table__.columns,
            (CounselResponse.id != None).label("has_response")
        )
        .join(CounselUser)
        .outerjoin(CounselResponse)
        .where(
            CounselUser.user_id == current_user.id,
            CounselUser.display == True
        )
    )

    count_stmt = select(func.count()).select_from(base_stmt.subquery())
    total = db.execute(count_stmt).scalar()

    data_stmt = (
        base_stmt
        .order_by(Counsel.id.desc())
        .offset(skip)
        .limit(limit)
    )

    counsel_list = db.execute(data_stmt).mappings().all()

    return total, counsel_list


def get_counsel(db: Session, current_user: User | Admin, id: int):

    stmt = (
        select(Counsel)
        .join(CounselUser)
        .options(
            selectinload(Counsel.content),
            selectinload(Counsel.response),
        )
        .where(
            Counsel.id == id,
            CounselUser.user_id == current_user.id,
            CounselUser.display == True,
            Counsel.enable == True,
        )
    )

    return db.execute(stmt).scalars().first()

def set_counsel(db: Session,  current_user: User | Admin, counsel_data: counsel_schema.CounselCreate):
    title = counsel_data.title.strip() if counsel_data.title else ""
    if not title:
        title = f"앱 상담 요청 ({datetime.now().strftime('%m-%d')})"

    counsel = Counsel(
        branch_id=current_user.branch_id,
        title=title,
        question_course=counsel_data.question_course,
        execute_date=datetime.now(),
        type='D'
    )
    db.add(counsel)
    db.commit()
    db.refresh(counsel)

    # 2. CounselUser 객체 생성 (이제 counsel.id 사용 가능)
    counselUser = CounselUser(
        counsel_id=counsel.id,  # 오타가 counsel_id 가 아니라 counse_id 이거 맞는지 확인!
        user_id=current_user.id
    )
    db.add(counselUser)
    db.commit()

    counselContent = CounselContent(
        id=counsel.id,
        content=counsel_data.content,
    )

    db.add(counselContent)
    db.commit()

    return counsel.id

def set_counsel_not_display(db: Session, current_user: User | Admin, id: int):
    query = db.query(CounselUser).filter(
        CounselUser.counsel_id == id
    )

    if not isinstance(current_user, Admin):
        query = query.filter(CounselUser.user_id == current_user.id)

    query.update(
        {CounselUser.display: False},
        synchronize_session=False
    )

    db.commit()
    return True
