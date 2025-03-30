from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.trainer import trainer_schema, trainer_crud
from starlette import status
from default_func import get_current_user

router = APIRouter(
    prefix="/trainers",
)

@router.get("/", response_model=trainer_schema.TrainerList, dependencies=[Depends(get_current_user)])
def trainer_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10):
    total, _trainer_list = trainer_crud.get_trainer_list(
        db, skip=page*size, limit=size)
    return {
        'total': total,
        'trainer_list': _trainer_list
    }

@router.get("/{trainer_id}", response_model=trainer_schema.Trainer, dependencies=[Depends(get_current_user)])
def trainer_detail(trainer_id: int, db: Session = Depends(get_db)):
    trainer = trainer_crud.get_trainer(db, trainer_id=trainer_id)

    if trainer is None:
        raise HTTPException(status_code=404, detail="trainer not found")

    return trainer