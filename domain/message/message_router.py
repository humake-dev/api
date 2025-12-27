from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from domain.message import message_schema, message_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/messages",dependencies=[Depends(get_current_user)])

@router.get("/", response_model=message_schema.MessageList)
def message_list(db: Session = Depends(get_db), current_user: User | Admin = Depends(get_current_user), page: int = 0, size: int = 10):
    total, _message_list = message_crud.get_message_list(db, current_user, skip=page*size, limit=size)
    return {
        'total': total,
        'message_list': _message_list
    }

@router.get("/{message_id}", response_model=message_schema.MessageContent)
def message_detail(message_id: int, current_user: User | Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    message = message_crud.get_message(db, current_user, id=message_id)

    if message is None:
        raise HTTPException(status_code=404, detail="messag not found")

    return message

@router.post("/hide/{message_id}")
def message_hide(message_id: int, current_user: User | Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    message = message_crud.get_message(db, current_user, id=message_id)

    if message is None:
        raise HTTPException(status_code=404, detail="messag not found")

    message_crud.set_messsage_not_display(db, current_user, id=message.id)

    return {"message": "Message hide"}

@router.post("/read/{message_id}")
def message_hide(message_id: int, current_user: User | Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    message = message_crud.get_message(db, current_user, id=message_id)

    if message is None:
        raise HTTPException(status_code=404, detail="messag not found")

    message_crud.set_messsage_read(db, current_user, id=message.id)

    return {"message": "Message read"}