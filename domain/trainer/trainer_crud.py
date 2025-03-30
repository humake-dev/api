from datetime import datetime
from models import Trainer
from sqlalchemy.orm import Session

def get_trainer_list(db: Session, skip: int = 0, limit: int = 10):
    _trainer_list = db.query(Trainer).order_by(Trainer.id.desc())

    total = _trainer_list.count()
    trainer_list = _trainer_list.offset(skip).limit(limit).all()
    return total, trainer_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_trainer(db: Session, trainer_id: int):
    trainer = db.query(Trainer).get(trainer_id)
    return trainer