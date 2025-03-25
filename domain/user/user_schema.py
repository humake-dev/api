import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    title: str
    created_at: datetime.datetime

