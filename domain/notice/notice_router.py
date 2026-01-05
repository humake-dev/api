from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from domain.notice import notice_schema, notice_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/notices",dependencies=[Depends(get_current_user)])

@router.get("", response_model=notice_schema.NoticeList)
def notice_list(db: Session = Depends(get_db), current_user: User | Admin = Depends(get_current_user), page: int = 0, size: int = 10):
    total, _notice_list = notice_crud.get_notice_list(db, current_user, skip=page*size, limit=size)
    return {
        'total': total,
        'notice_list': _notice_list
    }

@router.get("/{notice_id}", response_model=notice_schema.NoticeContent)
def notice_detail(notice_id: int, current_user: User | Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    notice = notice_crud.get_notice(db, current_user, id=notice_id)

    if notice is None:
        raise HTTPException(status_code=404, detail="notice not found")

    return notice