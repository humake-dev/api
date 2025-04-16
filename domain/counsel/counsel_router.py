from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.counsel import counsel_schema, counsel_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/counsels",dependencies=[Depends(get_session)])

@router.get("/", response_model=counsel_schema.CounselList)
def counsel_list(db: Session = Depends(get_db), session: dict = Depends(get_session), page: int = 0, size: int = 10):
    total, _counsel_list = counsel_crud.get_counsel_list(db, session, skip=page*size, limit=size)
    return {
        'total': total,
        'counsel_list': _counsel_list
    }

@router.get("/{counsel_id}", response_model=counsel_schema.CounselContent)
def counsel_detail(counsel_id: int, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    counsel = counsel_crud.get_counsel(db, session, id=counsel_id)

    if counsel is None:
        raise HTTPException(status_code=404, detail="counsel not found")

    return counsel

@router.post("/")
def create_counsel(_counsel_create: counsel_schema.CounselCreate,db: Session = Depends(get_db), session: dict = Depends(get_session)):
    counsel_id=counsel_crud.set_counsel(db, session, counsel_data=_counsel_create)
    return counsel_id

@router.post("/hide/{counsel_id}")
def counsel_hide(counsel_id: int, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    counsel = counsel_crud.get_counsel(db, session, id=counsel_id)

    if counsel is None:
        raise HTTPException(status_code=404, detail="messag not found")

    counsel_crud.set_counsel_not_display(db, session, id=counsel.id)

    return {"counsel": "Counsel hide"}