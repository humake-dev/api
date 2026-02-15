from datetime import datetime
from models import Branch, BranchPicture, Admin, User
from sqlalchemy.orm import Session
from sqlalchemy import select, func

def get_branch(db: Session, current_user: User | Admin, id: int = None):
    branch_id = id if isinstance(current_user, Admin) and id is not None else current_user.branch_id

    branch = db.query(Branch).join(BranchPicture, isouter=True).filter(Branch.id == branch_id).first()

    return branch
