from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from domain.reservation import reservation_schema, reservation_crud
from starlette import status
from typing import Optional
from default_func import *
from datetime import date
import calendar

router = APIRouter(prefix="/reservations",dependencies=[Depends(get_current_user)])

@router.get("", response_model=reservation_schema.ReservationList)
def reservation_list(
            db: Session = Depends(get_db),
            current_user: User | Admin = Depends(get_current_user),
            year: Optional[int] = None,
            month: Optional[int] = None,
            day: Optional[int] = None,
            page: int = 0,
            size: int = 10,
    ):
        today = date.today()

        # ─────────────────────────────
        # 1️⃣ year 기본값 + validation
        # ─────────────────────────────
        if year is None:
            year = today.year

        min_year = today.year - 10
        if not (min_year <= year <= today.year):
            raise HTTPException(
                status_code=400,
                detail=f"year must be between {min_year} and {today.year}",
            )

        # ─────────────────────────────
        # 2️⃣ month 기본값 + validation
        # ─────────────────────────────
        if month is None:
            month = today.month

        if not (1 <= month <= 12):
            raise HTTPException(
                status_code=400,
                detail="month must be between 1 and 12",
            )

        # ─────────────────────────────
        # 3️⃣ day validation (존재하는 날짜인지)
        # ─────────────────────────────
        if day is not None:
            _, last_day = calendar.monthrange(year, month)

            if not (1 <= day <= last_day):
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid date: {year}-{month:02d}-{day:02d}",
                )

        # ─────────────────────────────
        # 4️⃣ filters 구성
        # ─────────────────────────────
        filters = {
            "year": year,
            "month": month,
        }

        if day is not None:
            filters["day"] = day

        # ─────────────────────────────
        # 5️⃣ 데이터 조회
        # ─────────────────────────────
        total, _reservation_list = reservation_crud.get_reservation_list(
            db,
            current_user,
            filters=filters,
            skip=page * size,
            limit=size,
        )

        return {
            "total": total,
            "reservation_list": _reservation_list,
        }


@router.get("/{reservation_id}", response_model=reservation_schema.Reservation)
def reservation_detail(reservation_id: int, current_user: User | Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    reservation = reservation_crud.get_reservation(db, current_user, id=reservation_id)

    if reservation is None:
        raise HTTPException(status_code=404, detail="reservation not found")

    return reservation