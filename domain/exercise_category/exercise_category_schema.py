import datetime
from typing import Optional
from pydantic import BaseModel


class ExerciseCategoryPicture(BaseModel):
    id: int
    picture_url: str

class ExerciseCategory(BaseModel):
    id: int
    title: str
    created_at: datetime.datetime
    picture:  Optional[ExerciseCategoryPicture] = None

class ExerciseCategoryList(BaseModel):
    total: int = 0
    exercise_category_list: list[ExerciseCategory] = []

