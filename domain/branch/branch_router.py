from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.branch import branch_schema, branch_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/branches",dependencies=[Depends(get_session)])

@router.get("/", response_model=branch_schema.Branch)
def branch_detail(session: dict = Depends(get_session), db: Session = Depends(get_db)):
    branch = branch_crud.get_branch(db, session)

    if branch is None:
        raise HTTPException(status_code=404, detail="branch not found")

    return branch
