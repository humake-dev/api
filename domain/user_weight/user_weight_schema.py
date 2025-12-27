import datetime
from pydantic import BaseModel

class UserWeight(BaseModel):
    avg_weight: float
    group_date: str
    model_config = {
        "from_attributes": True
    }

class UserWeightList(BaseModel):
    total: int = 0
    user_weight_list: list[UserWeight] = []

class UserWeightCreate(BaseModel):
    weight : float
    model_config = {
        "from_attributes": True
    }