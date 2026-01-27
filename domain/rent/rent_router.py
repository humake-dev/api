from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from domain.rent import rent_schema, rent_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/rents",dependencies=[Depends(get_current_user)])

@router.get("", response_model=rent_schema.RentList)
def rent_list(db: Session = Depends(get_db), current_user: User | Admin = Depends(get_current_user), page: int = 0, size: int = 10, user_id: int | None = None):

    # user_id로 다른 유저 조회 시도
    if user_id is not None:
        # admin만 허용
        if not isinstance(current_user, Admin):
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        total, _rent_list = rent_crud.get_rent_list( db, current_user, skip=page*size, limit=size, user_id=user_id)
    # 자기 자신 조회
    else:
        total, _rent_list = rent_crud.get_rent_list( db, current_user, skip=page*size, limit=size)


    return {
        'total': total,
        'rent_list': _rent_list
    }

@router.get("/{rent_id}", response_model=rent_schema.Rent)
def rent_detail(rent_id: int, current_user: User | Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    rent = rent_crud.get_rent(db, current_user, id=rent_id)

    if rent is None:
        raise HTTPException(status_code=404, detail="rent_id not found")

    return rent