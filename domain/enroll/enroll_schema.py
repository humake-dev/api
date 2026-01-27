import datetime

from typing import Optional
from pydantic import BaseModel

class Enroll(BaseModel):
    id: int
    start_date : datetime.date
    end_date : datetime.date
    product_title : str
    trainer_name: Optional[str] = None
    model_config = {
        "from_attributes": True
    }

class EnrollList(BaseModel):
    total: int = 0
    enroll_list: list[Enroll] = []