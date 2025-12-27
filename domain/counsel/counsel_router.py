from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from domain.counsel import counsel_schema, counsel_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/counsels",dependencies=[Depends(get_current_user)])

@router.get("/", response_model=counsel_schema.CounselList)
def counsel_list(db: Session = Depends(get_db), current_user: User | Admin = Depends(get_current_user), page: int = 0, size: int = 10):
    total, _counsel_list = counsel_crud.get_counsel_list(db, current_user, skip=page*size, limit=size)
    return {
        'total': total,
        'counsel_list': _counsel_list
    }

@router.get("/{counsel_id}", response_model=counsel_schema.CounselContent)
def counsel_detail(counsel_id: int, current_user: User | Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    counsel = counsel_crud.get_counsel(db, current_user, id=counsel_id)

    if counsel is None:
        raise HTTPException(status_code=404, detail="counsel not found")

    return counsel

@router.post("/")
def create_counsel(_counsel_create: counsel_schema.CounselCreate,db: Session = Depends(get_db), current_user: User | Admin = Depends(get_current_user)):
    counsel_id=counsel_crud.set_counsel(db, current_user, counsel_data=_counsel_create)
    return counsel_id

@router.post("/hide/{counsel_id}")
def counsel_hide(counsel_id: int, current_user: User | Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    counsel = counsel_crud.get_counsel(db, current_user, id=counsel_id)

    if counsel is None:
        raise HTTPException(status_code=404, detail="messag not found")

    counsel_crud.set_counsel_not_display(db, current_user, id=counsel.id)

    return {"counsel": "Counsel hide"}