from models import Trainer,UserTrainer
from sqlalchemy.orm import Session
from sqlalchemy import case, select, desc

def get_trainer_list(db: Session, session: dict, skip: int = 0, limit: int = 10):
    _user_trainer_list = db.query(UserTrainer).filter(UserTrainer.user_id == session['user_id'])
    user_trainer_count= _user_trainer_list.count()

    _trainer_list = db.query(Trainer).join(Trainer.picture, isouter=True).filter(
        Trainer.branch_id == session['branch_id'], Trainer.is_trainer == True, Trainer.enable == True,
        Trainer.status == 'H')

    total = _trainer_list.count()
    if user_trainer_count:
        trainer_list = _trainer_list.order_by(case((Trainer.id == _user_trainer_list.first().trainer_id, 0), else_=1),  # 우선순위 지정: target_id는 0
        desc(Trainer.id)  # 나머지는 id 내림차순 정렬
        ).offset(skip).limit(limit).all()
    else:
        trainer_list = _trainer_list.order_by(Trainer.id.desc()).offset(skip).limit(limit).all()

    return total, trainer_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_trainer(db: Session, session: dict, id: int):
    trainer = db.query(Trainer).get(id)
    return trainer