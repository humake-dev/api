from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from domain.user_weight import user_weight_schema, user_weight_crud
from starlette import status
from typing import Optional
from default_func import *

router = APIRouter(prefix="/user_weights",dependencies=[Depends(get_current_user)])

@router.get("/", response_model=user_weight_schema.UserWeightList)
def user_weight_list(db: Session = Depends(get_db), current_user: User | Admin = Depends(get_current_user), month: Optional[int] = None, week: Optional[int] = None, page: int = 0, size: int = 10):
    filters = {}

    if month is not None:
        filters["month"] = month

    if week is not None:
        filters["week"] = week

    total, _user_weight_list = user_weight_crud.get_user_weight_list(db, current_user, filters=filters, skip=page*size, limit=size)
    return {
        'total': total,
        'user_weight_list': _user_weight_list
    }

@router.post("/")
def create_user_weight(_user_weight_create: user_weight_schema.UserWeightCreate,db: Session = Depends(get_db), current_user: User | Admin = Depends(get_current_user)):
    user_weight_id=user_weight_crud.set_user_weight(db, current_user, user_weight_data=_user_weight_create)
    return user_weight_id
