import datetime
from pydantic import BaseModel

class UserWeight(BaseModel):
    id: int
    user_id: int
    weight: float
    created_at: datetime.datetime
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