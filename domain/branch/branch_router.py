from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from starlette import status

from domain.branch import branch_schema, branch_crud
from default_func import get_db, get_current_user
from models import Admin, User

router = APIRouter(
    prefix="/branches",
    dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=List[branch_schema.Branch])
def branch_list(
    db: Session = Depends(get_db),
    current_user:  Admin = Depends(get_current_user),
):
    if not isinstance(current_user, Admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )

    return branch_crud.get_branches(db)

@router.get("/me", response_model=branch_schema.Branch)
def my_branch(
    db: Session = Depends(get_db),
    current_user: User | Admin = Depends(get_current_user),
):
    branch = branch_crud.get_branch_by_id(db, current_user.branch_id)

    if branch is None:
        raise HTTPException(status_code=404, detail="branch not found")

    return branch

@router.get("/{branch_id}", response_model=branch_schema.Branch)
def branch_detail(
    branch_id: int,
    db: Session = Depends(get_db),
    current_user: Admin = Depends(get_current_user),
):
    if not isinstance(current_user, Admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )

    branch = branch_crud.get_branch_by_id(db, branch_id)

    if branch is None:
        raise HTTPException(status_code=404, detail="branch not found")

    return branch




