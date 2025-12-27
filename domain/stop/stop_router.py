from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from domain.stop import stop_schema, stop_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/stops",dependencies=[Depends(get_current_user)])

@router.get("/", response_model=stop_schema.StopList)
def stop_list(db: Session = Depends(get_db), current_user: User | Admin = Depends(get_current_user), page: int = 0, size: int = 10):
    total, _stop_list = stop_crud.get_stop_list( db, current_user, skip=page*size, limit=size)
    return {
        'total': total,
        '_top_list': _stop_list
    }

@router.get("/{stop_id}", response_model=stop_schema.Stop)
def stop_detail(stop_id: int, current_user: User | Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    stop = stop_crud.get_stop(db, current_user, id=stop_id)

    if stop is None:
        raise HTTPException(status_code=404, detail="stop not found")

    return stop

@router.post("/")
def create_stop(_stop_create: stop_schema.StopCreate,db: Session = Depends(get_db), current_user: User | Admin = Depends(get_current_user)):
    stop_id=stop_crud.set_stop(db, current_user, stop_data=_stop_create)
    return stop_id