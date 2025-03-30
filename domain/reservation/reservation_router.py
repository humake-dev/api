from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.reservation import reservation_schema, reservation_crud
from starlette import status
from default_func import get_current_user

router = APIRouter(
    prefix="/reservations",
)

@router.get("/", response_model=reservation_schema.ReservationList, dependencies=[Depends(get_current_user)])
def reservation_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10, user_id: int = Depends(get_current_user)):
    total, _reservation_list = reservation_crud.get_reservation_list(
        db, user_id=user_id, skip=page*size, limit=size)
    return {
        'total': total,
        'reservation_list': _reservation_list
    }

@router.get("/{reservation_id}", response_model=reservation_schema.Reservation, dependencies=[Depends(get_current_user)])
def reservation_detail(reservation_id: int,user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    reservation = reservation_crud.get_reservation(db, user_id=user_id, reservation_id=reservation_id)

    if reservation is None:
        raise HTTPException(status_code=404, detail="reservation not found")

    return reservation