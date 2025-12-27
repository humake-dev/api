import datetime
from pydantic import BaseModel
from typing import Optional

class Reservation(BaseModel):
    id: int
    start_time: datetime.datetime
    end_time: datetime.datetime
    enable : bool
    created_at: datetime.datetime
    model_config = {
        "from_attributes": True
    }

class ReservationListResponse(BaseModel):
    id: int
    user_id: int
    trainer_name : str
    start_time: datetime.datetime
    end_time: datetime.datetime
    complete : int
    complete_at: Optional[datetime.datetime]
    created_at: datetime.datetime

class ReservationList(BaseModel):
    total: int = 0
    reservation_list: list[ReservationListResponse] = []
