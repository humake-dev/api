from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from domain.user_height import user_height_schema, user_height_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/user_heights",dependencies=[Depends(get_current_user)])

@router.get("/", response_model=user_height_schema.UserHeight)
def user_height_detail(current_user: User | Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    user_height = user_height_crud.get_user_height(db, current_user)

    if user_height is None:
        raise HTTPException(status_code=404, detail="user_height not found")

    return user_height
    
@router.post("/")
def create_user_height(_user_height_create: user_height_schema.UserHeightCreate,db: Session = Depends(get_db), current_user: User | Admin = Depends(get_current_user)):
    user_height_id=user_height_crud.set_user_height(db, current_user, user_height_data=_user_height_create)
    return user_height_id
