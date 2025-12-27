from datetime import datetime
from models import Notice, NoticeContent, Admin, User
from sqlalchemy.orm import Session

def get_notice_list(db: Session, current_user: User | Admin, skip: int = 0, limit: int = 10):
    _notice_list = db.query(Notice).filter(Notice.branch_id == current_user.branch_id).order_by(Notice.id.desc())

    total = _notice_list.count()
    notice_list = _notice_list.offset(skip).limit(limit).all()
    return total, notice_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_notice(db: Session, current_user: User | Admin, id: int):
    notice = db.query(NoticeContent).join(Notice).filter(Notice.branch_id == current_user.branch_id).filter(Notice.id == id).first()
    return notice