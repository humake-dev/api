from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from domain.entrance import entrance_schema, entrance_crud
from starlette import status
from typing import Optional
from default_func import *

router = APIRouter(prefix="/entrances", dependencies=[Depends(get_current_user)])

@router.get("", response_model=entrance_schema.EntranceList)
def entrance_list(db: Session = Depends(get_db), current_user: User | Admin = Depends(get_current_user), year: Optional[int] = None, month: Optional[int] = None, page: int = 0, size: int = 10):

    filters = {}
    if year is not None:
        filters["year"] = year

    if month is not None:
        filters["month"] = month

    total, _entrance_list = entrance_crud.get_entrance_list(db, current_user, filters=filters, skip=page*size, limit=size)
    return {
        'total': total,
        'entrance_list': _entrance_list
    }

@router.get("/{entrance_id}", response_model=entrance_schema.Entrance)
def entrance_detail(entrance_id: int, current_user: User | Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    entrance = entrance_crud.get_entrance(db, current_user, id=entrance_id)

    if entrance is None:
        raise HTTPException(status_code=404, detail="entrance not found")

    return entrance

@router.post("")
def create_entrance(
    payload: entrance_schema.EntranceCreate,
    db: Session = Depends(get_db),
    current_user: User | Admin = Depends(get_current_user),
):
    user_id = payload.user_id or current_user.id

    if payload.user_id is not None and not isinstance(current_user, Admin):
        raise HTTPException(403)

    return entrance_crud.set_entrance(db, user_id)