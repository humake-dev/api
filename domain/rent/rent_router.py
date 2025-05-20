from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.rent import rent_schema, rent_crud
from starlette import status
from default_func import *

router = APIRouter(prefix="/rents",dependencies=[Depends(get_session)])

@router.get("/", response_model=rent_schema.RentList)
def rent_list(db: Session = Depends(get_db), session: dict = Depends(get_session), page: int = 0, size: int = 10):
    total, _rent_list = rent_crud.get_rent_list( db, session, skip=page*size, limit=size)
    return {
        'total': total,
        'rent_list': _rent_list
    }

@router.get("/{rent_id}", response_model=rent_schema.Rent)
def rent_detail(rent_id: int, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    rent = rent_crud.get_rent(db, session, id=rent_id)

    if rent is None:
        raise HTTPException(status_code=404, detail="rent_id not found")

    return rent