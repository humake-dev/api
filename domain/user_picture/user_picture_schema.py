
from pydantic import BaseModel
from typing import Optional
import datetime


class UserPictureCreate(BaseModel):
	id: int
	picture_url: str

class UserPicture(BaseModel):
	id: int
	picture_url: str
	created_at: datetime.datetime
	updated_at: datetime.datetime

