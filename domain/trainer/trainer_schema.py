import datetime

from typing import Optional
from pydantic import BaseModel


class TrainerPicture(BaseModel):
    id: int
    picture_url: str

class Trainer(BaseModel):
    id: int
    branch_id: int
    name: str
    created_at: datetime.datetime
    picture:  Optional[TrainerPicture] = None

class TrainerList(BaseModel):
    total: int = 0
    trainer_list: list[Trainer] = []