import datetime
from pydantic import BaseModel, Field

class StopBase(BaseModel):
    id: int
    user_id: int
    stop_start_date: datetime.date
    stop_end_date: datetime.date
    created_at: datetime.datetime

    model_config = {
        "from_attributes": True
    }

class StopListItem(StopBase):
    pass

class StopList(BaseModel):
    total: int = 0
    stop_list: list[StopListItem] = Field(default_factory=list)

class StopDetail(StopBase):
    description: str

class StopCreate(BaseModel):
    stop_start_date : datetime.date
    stop_end_date : datetime.date
    description : str
    model_config = {
        "from_attributes": True
    }