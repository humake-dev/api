import datetime

from typing import Optional
from pydantic import BaseModel

class Rent(BaseModel):
    id: int
    start_date : datetime.date
    end_date: datetime.date
    no : int
    product_title : str
    model_config = {
        "from_attributes": True
    }

class RentList(BaseModel):
    total: int = 0
    rent_list: list[Rent] = []