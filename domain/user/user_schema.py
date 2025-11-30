import datetime
from typing import Optional
from pydantic import BaseModel
from domain.trainer.trainer_schema import Trainer

class UserPicture(BaseModel):
    id: int
    picture_url: str

class UserAccessCard(BaseModel):
    id: int
    card_no: str

class UserHeight(BaseModel):
    id: int
    height: float

class UserWeight(BaseModel):
    id: int
    weight: float

class User(BaseModel):
    id: int
    branch_id: int
    name: str
    phone : str
    created_at: datetime.datetime
    picture: Optional[UserPicture] = None
    access_card: Optional[UserAccessCard] = None
    trainer : Optional[Trainer] = None
    user_height : Optional[UserHeight] = None
    user_weight : Optional[UserWeight] = None
