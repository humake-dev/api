import datetime
from pydantic import BaseModel

class Stop(BaseModel):
    id: int
    user_id: int
    stop_start_date: datetime.date
    stop_end_date: datetime.date
    created_at: datetime.datetime

    model_config = {
        "from_attributes": True
    }

class StopList(BaseModel):
    total: int = 0
    stop_list: list[Stop] = []

class StopCreate(BaseModel):
    stop_start_date : datetime.date
    stop_end_date : datetime.date
    description : str
    model_config = {
        "from_attributes": True
    }