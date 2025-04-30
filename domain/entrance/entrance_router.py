from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.entrance import entrance_schema, entrance_crud
from starlette import status
from typing import Optional
from default_func import *

router = APIRouter(prefix="/entrances", dependencies=[Depends(get_session)])

@router.get("/", response_model=entrance_schema.EntranceList)
def entrance_list(db: Session = Depends(get_db), session: dict = Depends(get_session), year: Optional[int] = None, month: Optional[int] = None, page: int = 0, size: int = 10):

    filters = {}
    if year is not None:
        filters["year"] = year

    if month is not None:
        filters["month"] = month

    total, _entrance_list = entrance_crud.get_entrance_list(db, session, filters=filters, skip=page*size, limit=size)
    return {
        'total': total,
        'entrance_list': _entrance_list
    }

@router.get("/{entrance_id}", response_model=entrance_schema.Entrance)
def entrance_detail(entrance_id: int, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    entrance = entrance_crud.get_entrance(db, session, id=entrance_id)

    if entrance is None:
        raise HTTPException(status_code=404, detail="entrance not found")

    return entrance