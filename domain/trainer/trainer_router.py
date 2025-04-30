from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.trainer import trainer_schema, trainer_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/trainers",dependencies=[Depends(get_session)])

@router.get("/", response_model=trainer_schema.TrainerList)
def trainer_list(db: Session = Depends(get_db), session: dict = Depends(get_session), page: int = 0, size: int = 10):
    total, _trainer_list = trainer_crud.get_trainer_list( db, session, skip=page*size, limit=size)
    return {
        'total': total,
        'trainer_list': _trainer_list
    }

@router.get("/{trainer_id}", response_model=trainer_schema.Trainer)
def trainer_detail(trainer_id: int, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    trainer = trainer_crud.get_trainer(db, session, id=trainer_id)

    if trainer is None:
        raise HTTPException(status_code=404, detail="trainer not found")

    return trainer