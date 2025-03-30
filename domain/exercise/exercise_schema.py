import datetime
from pydantic import BaseModel


class Exercise(BaseModel):
    id: int
    title: str
    created_at: datetime.datetime

class ExerciseList(BaseModel):
    total: int = 0
    exercise_list: list[Exercise] = []
