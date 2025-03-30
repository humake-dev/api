import datetime
from pydantic import BaseModel


class ExerciseCategory(BaseModel):
    id: int
    title: str
    created_at: datetime.datetime

class ExerciseCategoryList(BaseModel):
    total: int = 0
    exercise_category_list: list[ExerciseCategory] = []
