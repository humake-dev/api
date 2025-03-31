import datetime
from pydantic import BaseModel


class Notice(BaseModel):
    id: int
    branch_id: int
    title: str
    created_at: datetime.datetime

class NoticeList(BaseModel):
    total: int = 0
    notice_list: list[Notice] = []
