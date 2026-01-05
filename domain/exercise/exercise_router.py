from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from domain.exercise import exercise_schema, exercise_crud
from starlette import status
from typing import Optional
from default_func import *

router = APIRouter(prefix="/exercises", dependencies=[Depends(get_current_user)])

@router.get("", response_model=exercise_schema.ExerciseList)
def exercise_list(
        db: Session = Depends(get_db),
        exercise_category_id: Optional[int] = None,
        page: int = 0,
        size: int = 10
):
    filters = {}
    if exercise_category_id is not None:
        filters["exercise_category_id"] = exercise_category_id

    total, _exercise_list = exercise_crud.get_exercise_list(db, filters=filters, skip=page * size, limit=size)

    return {
        "total": total,
        "exercise_list": _exercise_list
    }

@router.get("/{exercise_id}", response_model=exercise_schema.Exercise)
def exercise_detail(exercise_id: int, db: Session = Depends(get_db)):
    exercise = exercise_crud.get_exercise(db, id=exercise_id)

    if exercise is None:
        raise HTTPException(status_code=404, detail="exercise not found")

    return exercise