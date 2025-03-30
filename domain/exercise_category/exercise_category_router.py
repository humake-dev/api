from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.exercise_category import exercise_category_schema, exercise_category_crud
from starlette import status
from default_func import get_current_user

router = APIRouter(
    prefix="/exercise_categories",
)

@router.get("/", response_model=exercise_category_schema.ExerciseCategoryList, dependencies=[Depends(get_current_user)])
def exercise_category_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10):
    total, _exercise_category_list = exercise_category_crud.get_exercise_category_list(
        db, skip=page*size, limit=size)
    return {
        'total': total,
        'exercise_category_list': _exercise_category_list
    }

@router.get("/{exercise_category_id}", response_model=exercise_category_schema.ExerciseCategory, dependencies=[Depends(get_current_user)])
def exercise_category_detail(exercise_category_id: int, db: Session = Depends(get_db)):
    exercise_category= exercise_category_crud.get_exercise_category(db, exercise_category_id=exercise_category_id)

    if exercise_category is None:
        raise HTTPException(status_code=404, detail="exercise_category not found")

    return exercise_category