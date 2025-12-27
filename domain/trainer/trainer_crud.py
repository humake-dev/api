from models import Trainer,UserTrainer, Admin, User
from sqlalchemy.orm import Session
from sqlalchemy import case, select, desc


def get_trainer_list(
    db: Session,
    current_user: User | Admin,
    skip: int = 0,
    limit: int = 10
):
    user_trainer_id = None

    # User인 경우만 자신의 트레이너 조회
    if not isinstance(current_user, Admin):
        user_trainer = (
            db.query(UserTrainer.trainer_id)
            .filter(UserTrainer.user_id == current_user.id)
            .first()
        )
        if user_trainer:
            user_trainer_id = user_trainer.trainer_id

    # 공통 트레이너 쿼리
    base_query = (
        db.query(Trainer)
        .join(Trainer.picture, isouter=True)
        .filter(
            Trainer.branch_id == current_user.branch_id,
            Trainer.is_trainer.is_(True),
            Trainer.enable.is_(True),
            Trainer.status == "H",
        )
    )

    total = base_query.count()

    # User + 트레이너 연결 있음 → 우선 정렬
    if user_trainer_id is not None:
        trainer_list = (
            base_query
            .order_by(
                case(
                    (Trainer.id == user_trainer_id, 0),
                    else_=1
                ),
                Trainer.id.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    else:
        # Admin 또는 연결 없음
        trainer_list = (
            base_query
            .order_by(Trainer.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    return total, trainer_list

def get_trainer(db: Session, current_user: User | Admin, id: int):
    trainer = db.query(Trainer).filter(Trainer.branch_id == current_user.branch_id).filter(Trainer.id==id).first()
    return trainer