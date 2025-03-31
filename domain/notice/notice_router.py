from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.notice import notice_schema, notice_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/notices",dependencies=[Depends(get_session)])

@router.get("/", response_model=notice_schema.NoticeList)
def notice_list(db: Session = Depends(get_db), session: dict = Depends(get_session), page: int = 0, size: int = 10):
    total, _notice_list = notice_crud.get_notice_list(db, session, skip=page*size, limit=size)
    return {
        'total': total,
        'notice_list': _notice_list
    }

@router.get("/{notice_id}", response_model=notice_schema.Notice)
def notice_detail(notice_id: int, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    notice = notice_crud.get_notice(db, session, notice_id=notice_id)

    if notice is None:
        raise HTTPException(status_code=404, detail="notice not found")

    return notice