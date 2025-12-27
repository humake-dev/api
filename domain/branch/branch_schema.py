import datetime
from pydantic import BaseModel
from typing import Optional

class BranchPicture(BaseModel):
    id: int
    picture_url: str

class Branch(BaseModel):
    id: int
    title: str
    app_title_color: str
    app_notice_color: str
    created_at: datetime.datetime
    picture: Optional[BranchPicture] = None