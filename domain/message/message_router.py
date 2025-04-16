from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.message import message_schema, message_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/messages",dependencies=[Depends(get_session)])

@router.get("/", response_model=message_schema.MessageList)
def message_list(db: Session = Depends(get_db), session: dict = Depends(get_session), page: int = 0, size: int = 10):
    total, _message_list = message_crud.get_message_list(db, session, skip=page*size, limit=size)
    return {
        'total': total,
        'message_list': _message_list
    }

@router.get("/{message_id}", response_model=message_schema.MessageContent)
def message_detail(message_id: int, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    message = message_crud.get_message(db, session, id=message_id)

    if message is None:
        raise HTTPException(status_code=404, detail="messag not found")

    return message

@router.post("/hide/{message_id}")
def message_hide(message_id: int, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    message = message_crud.get_message(db, session, id=message_id)

    if message is None:
        raise HTTPException(status_code=404, detail="messag not found")

    message_crud.set_messsage_not_display(db, session, id=message.id)

    return {"message": "Message hide"}