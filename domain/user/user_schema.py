import datetime
from typing import Optional
from pydantic import BaseModel


class UserPicture(BaseModel):
    id: int
    picture_url: str

class UserAccessCard(BaseModel):
    id: int
    card_no: str

class User(BaseModel):
    id: int
    branch_id: int
    name: str
    created_at: datetime.datetime
    picture: Optional[UserPicture] = None
    access_card: Optional[UserAccessCard] = None

