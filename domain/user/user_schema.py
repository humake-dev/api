import datetime
from typing import Optional
from pydantic import BaseModel

class UserPicture(BaseModel):
    id: int
    picture_url: str

class User(BaseModel):
    id: int
    name: str
    created_at: datetime.datetime
    picture: Optional[UserPicture] = None

