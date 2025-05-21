import datetime
from pydantic import BaseModel
from models import UserDeviceOS

class UserDeviceCreate(BaseModel):
    os: UserDeviceOS
    token: str
    model_config = {
        "from_attributes": True
    }
