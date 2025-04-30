from datetime import datetime
from models import Branch, BranchPicture
from sqlalchemy.orm import Session
from sqlalchemy import select, func

def get_branch(db: Session, session: dict):
    base_stmt = (
        select(Branch.id, Branch.title, Branch.app_title_color, Branch.app_notice_color , BranchPicture.picture_url, Branch.created_at).select_from(Branch).join(BranchPicture).where(
            Branch.id == session['branch_id'], Branch.enable == True)
    )
    branch = db.execute(base_stmt).mappings().first()

    return branch
