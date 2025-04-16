import datetime
from pydantic import BaseModel

class Message(BaseModel):
    id: int
    branch_id: int
    title: str
    created_at: datetime.datetime
    model_config = {
        "from_attributes": True
    }

class MessageContent(BaseModel):
    id: int
    content : str
    model_config = {
        "from_attributes": True
    }

class MessageList(BaseModel):
    total: int = 0
    message_list: list[Message] = []
