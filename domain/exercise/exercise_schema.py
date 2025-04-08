import datetime
from typing import Optional
from pydantic import BaseModel


class ExercisePicture(BaseModel):
    id: int
    picture_url: str

class Exercise(BaseModel):
    id: int
    exercise_category_id : int
    title: str
    content : str
    created_at: datetime.datetime
    picture:  Optional[ExercisePicture] = None

class ExerciseList(BaseModel):
    total: int = 0
    exercise_list: list[Exercise] = []
