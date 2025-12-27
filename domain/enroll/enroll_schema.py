import datetime

from typing import Optional
from pydantic import BaseModel

class Enroll(BaseModel):
    id: int
    start_date : datetime.date
    end_date : datetime.date

class EnrollList(BaseModel):
    total: int = 0
    enroll_list: list[Enroll] = []