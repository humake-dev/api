from models import Stop
from sqlalchemy.orm import Session
from domain.stop import stop_schema

def get_stop_list(db: Session, session: dict, skip: int = 0, limit: int = 10):
    _stop_list = db.query(Stop).filter(Stop.user_id == session['user_id']).order_by(Stop.id.desc())

    total = _stop_list.count()
    stop_list = _stop_list.offset(skip).limit(limit).all()
    return total, stop_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_stop(db: Session, session: dict, id: int):
    stop = db.query(Stop).get(id)
    return stop

def set_stop(db: Session, session: dict, stop_data: stop_schema.StopCreate):
    stop = Stop(
        branch_id=session['branch_id'],
        title='앱에서의 요청',
        question_course=counsel_data.question_course,
        execute_date=datetime.now(),
        type='D'
    )
    db.add(stop)
    db.commit()
    db.refresh(counsel)

    # 2. CounselUser 객체 생성 (이제 counsel.id 사용 가능)
    counselUser = CounselUser(
        counsel_id=counsel.id,  # 오타가 counsel_id 가 아니라 counse_id 이거 맞는지 확인!
        user_id=session['user_id']
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