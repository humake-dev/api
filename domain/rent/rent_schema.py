import datetime

from typing import Optional
from pydantic import BaseModel

class Rent(BaseModel):
    id: int
    start_datetime : datetime.datetime
    end_datetime : datetime.datetime

class RentList(BaseModel):
    total: int = 0
    rent_list: list[Rent] = []