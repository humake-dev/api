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
    base_stmt = (
        select(Message.id, Message.title,  MessageContent.content, MessageUser.readtime, Message.created_at).select_from(MessageContent).join(Message).join(MessageUser).where(
            Message.id == id, MessageUser.user_id == session['user_id'], Message.enable == True)
    )

    message = db.execute(base_stmt).mappings().first()

    return message

def set_messsage_not_display(db: Session, session: dict, id: int):
    db.query(MessageUser).filter(MessageUser.message_id == id).update({MessageUser.display: False})
    db.commit()
    return True

def set_messsage_read(db: Session, session: dict, id: int):
    db.query(MessageUser).filter(MessageUser.message_id == id).update({MessageUser.readtime: datetime.utcnow()})
    db.commit()
    return True