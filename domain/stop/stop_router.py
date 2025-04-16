from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.stop import stop_schema, stop_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/stops",dependencies=[Depends(get_session)])

@router.get("/", response_model=stop_schema.StopList)
def stop_list(db: Session = Depends(get_db), session: dict = Depends(get_session), page: int = 0, size: int = 10):
    total, _stop_list = stop_crud.get_stop_list( db, session, skip=page*size, limit=size)
    return {
        'total': total,
        '_top_list': _stop_list
    }

@router.get("/{stop_id}", response_model=stop_schema.Stop)
def stop_detail(stop_id: int, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    stop = stop_crud.get_stop(db, session, id=stop_id)

    if stop is None:
        raise HTTPException(status_code=404, detail="stop not found")

    return stop

@router.post("/")
def create_stop(_stop_create: stop_schema.StopCreate,db: Session = Depends(get_db), session: dict = Depends(get_session)):
    stop_id=stop_crud.set_stop(db, session, stop_data=_stop_create)
    return stop_id