from datetime import datetime
from models import Branch
from sqlalchemy.orm import joinedload, Session

def get_branch_by_id(db: Session, branch_id: int):
    return (
        db.query(Branch)
        .options(joinedload(Branch.picture))
        .filter(Branch.id == branch_id)
        .first()
    )


def get_branches(db: Session):
    return (
        db.query(Branch)
        .options(joinedload(Branch.picture))
        .all()
    )
