import datetime
from pydantic import BaseModel

class Counsel(BaseModel):
    id: int
    branch_id: int
    title: str
    created_at: datetime.datetime
    model_config = {
        "from_attributes": True
    }

class CounselContent(BaseModel):
    id: int
    content : str
    model_config = {
        "from_attributes": True
    }

class CounselList(BaseModel):
    total: int = 0
    counsel_list: list[Counsel] = []

class CounselCreate(BaseModel):
    question_course: str
    content : str
    model_config = {
        "from_attributes": True
    }