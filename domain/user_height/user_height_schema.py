import datetime
from pydantic import BaseModel

class UserHeight(BaseModel):
    id: int
    user_id: int
    height: float
    created_at: datetime.datetime
    model_config = {
        "from_attributes": True
    }

class UserHeightCreate(BaseModel):
    height : float
    model_config = {
        "from_attributes": True
    }