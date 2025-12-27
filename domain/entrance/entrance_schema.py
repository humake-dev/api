import datetime
from pydantic import BaseModel


class Entrance(BaseModel):
    id: int
    in_time: datetime.datetime
    created_at: datetime.datetime
    model_config = {
        "from_attributes": True
    }

class EntranceList(BaseModel):
    total: int = 0
    entrance_list: list[Entrance] = []
