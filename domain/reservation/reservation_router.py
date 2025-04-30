from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.reservation import reservation_schema, reservation_crud
from starlette import status
from typing import Optional
from default_func import *

router = APIRouter(prefix="/reservations",dependencies=[Depends(get_session)])

@router.get("/", response_model=reservation_schema.ReservationList)
def reservation_list(db: Session = Depends(get_db), session: dict = Depends(get_session), year: Optional[int] = None, month: Optional[int] = None, day: Optional[str] = None, page: int = 0, size: int = 10):

    filters = {}
    if year is not None:
        filters["year"] = year

    if month is not None:
        filters["month"] = month

    if day is not None:
        filters["day"] = day

    total, _reservation_list = reservation_crud.get_reservation_list(db, session, filters=filters, skip=page*size, limit=size)
    return {
        'total': total,
        'reservation_list': _reservation_list
    }

@router.get("/{reservation_id}", response_model=reservation_schema.Reservation)
def reservation_detail(reservation_id: int, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    reservation = reservation_crud.get_reservation(db, session, id=reservation_id)

    if reservation is None:
        raise HTTPException(status_code=404, detail="reservation not found")

    return reservation