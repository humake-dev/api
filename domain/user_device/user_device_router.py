from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.user_device import user_device_schema, user_device_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/user-devices",dependencies=[Depends(get_session)])

@router.post("/")
def create_user_device(_user_device_create: user_device_schema.UserDeviceCreate,db: Session = Depends(get_db), session: dict = Depends(get_session)):
    user_device_id=user_device_crud.set_user_device(db, session, user_device_data=_user_device_create)
    return user_device_id
