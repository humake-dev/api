from datetime import datetime
from models import Branch, BranchPicture, Admin, User
from sqlalchemy.orm import Session
from sqlalchemy import select, func

def get_branch(db: Session, current_user: User | Admin, id: int = None):
    branch_id = id if isinstance(current_user, Admin) and id is not None else current_user.branch_id

    base_stmt = (
        select(Branch.id, Branch.title, Branch.app_title_color, Branch.app_notice_color , BranchPicture.picture_url, Branch.created_at).select_from(Branch).join(BranchPicture, isouter=True).where(
            Branch.id == branch_id, Branch.enable == True)
    )
    branch = db.execute(base_stmt).mappings().first()

    return branch
