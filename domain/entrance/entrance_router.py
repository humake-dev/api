from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from domain.entrance import entrance_schema, entrance_crud
from starlette import status
from typing import Optional
from default_func import *
from datetime import date
import calendar
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/entrances", dependencies=[Depends(get_current_user)])

@router.get("", response_model=entrance_schema.EntranceList)
def entrance_list(
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
    total, entrance_list = entrance_crud.get_entrance_list(
        db,
        current_user,
        filters=filters,
        skip=page * size,
        limit=size,
    )

    response_data = {
        "total": total,
        "entrance_list": entrance_list,
    }

    print("JSON RESPONSE >>>", jsonable_encoder(response_data))

    return response_data


@router.get("/{entrance_id}", response_model=entrance_schema.Entrance)
def entrance_detail(entrance_id: int, current_user: User | Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    entrance = entrance_crud.get_entrance(db, current_user, id=entrance_id)

    if entrance is None:
        raise HTTPException(status_code=404, detail="entrance not found")

    return entrance

@router.post("")
def create_entrance(
    payload: entrance_schema.EntranceCreate,
    db: Session = Depends(get_db),
    current_user: User | Admin = Depends(get_current_user),
):
    user_id = payload.user_id or current_user.id

    if payload.user_id is not None and not isinstance(current_user, Admin):
        raise HTTPException(403)

    return entrance_crud.set_entrance(db, user_id)