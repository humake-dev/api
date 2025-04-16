import datetime

from typing import Optional
from pydantic import BaseModel

class Stop(BaseModel):
    id: int
    user_id: int
    stop_start_date: str
    stop_end_date: str
    created_at: datetime.datetime

class StopList(BaseModel):
    total: int = 0
    stop_list: list[Stop] = []

class StopCreate(BaseModel):
    stop_start_date : str
    stop_end_date : str
    content : str
    model_config = {
        "from_attributes": True
    }