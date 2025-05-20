from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.enroll import enroll_schema, enroll_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/enrolls",dependencies=[Depends(get_session)])

@router.get("/", response_model=enroll_schema.EnrollList)
def enroll_list(db: Session = Depends(get_db), session: dict = Depends(get_session), page: int = 0, size: int = 10):
    total, _enroll_list = enroll_crud.get_enroll_list( db, session, skip=page*size, limit=size)
    return {
        'total': total,
        'enroll_list': _enroll_list
    }

@router.get("/{enroll_id}", response_model=enroll_schema.Enroll)
def enroll_detail(trainer_id: int, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    trainer = enroll_crud.get_enroll(db, session, id=trainer_id)

    if trainer is None:
        raise HTTPException(status_code=404, detail="enroll_id not found")

    return trainer