import datetime
from typing import Optional
from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    branch_id: int
    token_type: str = "bearer"

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

class RefreshTokenRequest(BaseModel):
    refresh_token: str

