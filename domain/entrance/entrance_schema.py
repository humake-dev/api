import datetime
from pydantic import BaseModel


class Entrance(BaseModel):
    id: int
    in_time: datetime.datetime
    created_at: datetime.datetime

class EntranceList(BaseModel):
    total: int = 0
    entrance_list: list[Entrance] = []
