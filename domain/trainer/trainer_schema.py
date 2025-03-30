import datetime

from pydantic import BaseModel


class Trainer(BaseModel):
    id: int
    name: str
    created_at: datetime.datetime

class TrainerList(BaseModel):
    total: int = 0
    trainer_list: list[Trainer] = []
