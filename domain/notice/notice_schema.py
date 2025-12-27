import datetime
from typing import Optional
from pydantic import BaseModel

class Notice(BaseModel):
    id: int
    branch_id: int
    title: str
    created_at: datetime.datetime
    model_config = {
        "from_attributes": True
    }


class NoticeContent(BaseModel):
    id: int
    content : str
    model_config = {
        "from_attributes": True
    }

class NoticeList(BaseModel):
    total: int = 0
    notice_list: list[Notice] = []
