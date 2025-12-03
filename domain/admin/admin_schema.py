import datetime
from typing import Optional
from pydantic import BaseModel

class AdminPicture(BaseModel):
    id: int
    picture_url: str

class Admin(BaseModel):
    id: int
    branch_id: int
    uid : str
    name: str
    encrypted_password : str
    created_at: datetime.datetime
    picture: Optional[AdminPicture] = None
