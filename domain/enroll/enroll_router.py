from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from domain.enroll import enroll_schema, enroll_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/enrolls",dependencies=[Depends(get_current_user)])

@router.get("", response_model=enroll_schema.EnrollList)
def enroll_list(db: Session = Depends(get_db), current_user: User | Admin = Depends(get_current_user), page: int = 0, size: int = 10, user_id: int | None = None, primary_only: bool = False):

    # user_id로 다른 유저 조회 시도
    if user_id is not None:
        # admin만 허용
        if not isinstance(current_user, Admin):
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        total, _enroll_list = enroll_crud.get_enroll_list( db, current_user, skip=page*size, limit=size, user_id=user_id,primary_only=primary_only)
    # 자기 자신 조회
    else:
        total, _enroll_list = enroll_crud.get_enroll_list( db, current_user, skip=page*size, limit=size,primary_only=primary_only)

    return {
        'total': total,
        'enroll_list': _enroll_list
    }

@router.get("/{enroll_id}", response_model=enroll_schema.Enroll)
def enroll_detail(enroll_id: int, current_user: User | Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    trainer = enroll_crud.get_enroll(db, current_user, id=enroll_id)

    if trainer is None:
        raise HTTPException(status_code=404, detail="enroll_id not found")

    return trainer