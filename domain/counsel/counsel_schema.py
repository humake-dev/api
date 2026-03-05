import datetime
from typing import Optional
from pydantic import BaseModel
from models import CounselQuestionCourse

class CounselResponse(BaseModel):
    content: str
    created_at: datetime.datetime

    model_config = {"from_attributes": True}

class CounselContent(BaseModel):
    content: str

    model_config = {"from_attributes": True}

class Counsel(BaseModel):
    id: int
    title: str
    created_at: datetime.datetime
    content: CounselContent
    response: CounselResponse| None = None

    model_config = {"from_attributes": True}

class CounselSummary(BaseModel):
    id: int
    title: str
    created_at: datetime.datetime
    has_response: bool

    model_config = {"from_attributes": True}

class CounselList(BaseModel):
    total: int = 0
    counsel_list: list[CounselSummary] = []

class CounselCreate(BaseModel):
    title: str | None = None
    question_course: CounselQuestionCourse
    content : str
    model_config = {
        "from_attributes": True
    }
