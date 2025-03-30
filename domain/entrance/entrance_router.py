from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.entrance import entrance_schema, entrance_crud
from starlette import status
from default_func import get_current_user

router = APIRouter(
    prefix="/entrances",
)

@router.get("/", response_model=entrance_schema.EntranceList, dependencies=[Depends(get_current_user)])
def entrance_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10, user_id: int = Depends(get_current_user)):
    total, _entrance_list = entrance_crud.get_entrance_list(
        db, user_id=user_id, skip=page*size, limit=size)
    return {
        'total': total,
        'entrance_list': _entrance_list
    }

@router.get("/{entrance_id}", response_model=entrance_schema.Entrance, dependencies=[Depends(get_current_user)])
def entrance_detail(entrance_id: int,user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    entrance = entrance_crud.get_entrance(db,user_id=user_id, entrance_id=entrance_id)

    if entrance is None:
        raise HTTPException(status_code=404, detail="entrance not found")

    return entrance