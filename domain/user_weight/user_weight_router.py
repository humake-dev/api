from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.user_weight import user_weight_schema, user_weight_crud
from starlette import status
from typing import Optional
from default_func import *

router = APIRouter(prefix="/user_weights",dependencies=[Depends(get_session)])

@router.get("/", response_model=user_weight_schema.UserWeightList)
def user_weight_list(db: Session = Depends(get_db), session: dict = Depends(get_session), month: Optional[int] = None, week: Optional[int] = None, page: int = 0, size: int = 10):
    filters = {}

    if month is not None:
        filters["month"] = month

    if week is not None:
        filters["week"] = week

    total, _user_weight_list = user_weight_crud.get_weight_list(db, session, filters=filters, skip=page*size, limit=size)
    return {
        'total': total,
        'user_weight_list': _user_weight_list
    }
