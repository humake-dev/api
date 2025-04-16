from datetime import datetime
from models import Message, MessageContent, MessageUser
from sqlalchemy.orm import Session
from sqlalchemy import select, func

def get_message_list(db: Session, session: dict, skip: int = 0, limit: int = 10):

    base_stmt = (
        select(*Message.__table__.columns).join(MessageUser).where(
            MessageUser.user_id == session['user_id'],MessageUser.display == True)
    )

    count_stmt = select(func.count()).select_from(base_stmt.subquery())
    total = db.execute(count_stmt).scalar()

    data_stmt = base_stmt.order_by(Message.id.desc()).offset(skip).limit(limit)
    message_list = db.execute(data_stmt).mappings().all()

    return total, message_list

def get_message(db: Session, session: dict, id: int):
    message = db.query(MessageContent).join(Message).join(MessageUser).filter(MessageUser.user_id == session['user_id']).filter(Message.id == id).first()
    return message

def set_messsage_not_display(db: Session, session: dict, id: int):
    db.query(MessageUser).filter(MessageUser.message_id == id).update({MessageUser.display: False})
    db.commit()
    return True