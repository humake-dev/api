import datetime
from pydantic import BaseModel


class Reservation(BaseModel):
    id: int
    start_time: datetime.datetime
    end_time: datetime.datetime
    created_at: datetime.datetime

class ReservationUserResponse(BaseModel):
    id: int
    user_id: int
    complete_at: datetime.datetime
    reservation: Reservation  # ✅ `Reservation` 포함

class ReservationList(BaseModel):
    total: int = 0
    reservation_list: list[ReservationUserResponse] = []
