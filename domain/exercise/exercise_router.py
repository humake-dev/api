from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.exercise import exercise_schema, exercise_crud
from starlette import status
from default_func import get_current_user

router = APIRouter(
    prefix="/exercises",
)

@router.get("/", response_model=exercise_schema.ExerciseList, dependencies=[Depends(get_current_user)])
def exercise_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10):
    total, _exercise_list = exercise_crud.get_exercise_list(
        db, skip=page*size, limit=size)
    return {
        'total': total,
        'exercise_list': _exercise_list
    }

@router.get("/{exercise_id}", response_model=exercise_schema.Exercise, dependencies=[Depends(get_current_user)])
def exercise_detail(exercise_id: int, db: Session = Depends(get_db)):
    exercise = exercise_crud.get_exercise(db, exercise_id=exercise_id)

    if exercise is None:
        raise HTTPException(status_code=404, detail="exercise not found")

    return exercise