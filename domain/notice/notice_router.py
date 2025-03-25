from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.notice import notice_schema, notice_crud
from starlette import status

router = APIRouter(
    prefix="/api/notice",
)

@router.get("/list", response_model=notice_schema.NoticeList)
def notice_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10):
    total, _notice_list = notice_crud.get_notice_list(
        db, skip=page*size, limit=size)
    return {
        'total': total,
        'notice_list': _notice_list
    }

@router.get("/detail/{notice_id}", response_model=notice_schema.Notice)
def notice_detail(notice_id: int, db: Session = Depends(get_db)):
    notice = notice_crud.get_notice(db, notice_id=notice_id)
    return notice