from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from domain.notice import notice_router
from domain.user import user_router
from domain.trainer import trainer_router
from domain.exercise import exercise_router
from domain.exercise_category import exercise_category_router
from domain.reservation import reservation_router
from domain.entrance import entrance_router
from domain.message import message_router
from domain.counsel import counsel_router
from domain.stop import stop_router

# from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="humake_api_is_good")

origins = [
    "http://127.0.0.1:5173",    # 또는 "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notice_router.router)
app.include_router(user_router.router)
app.include_router(trainer_router.router)
app.include_router(exercise_router.router)
app.include_router(exercise_category_router.router)
app.include_router(reservation_router.router)
app.include_router(entrance_router.router)
app.include_router(message_router.router)
app.include_router(counsel_router.router)
app.include_router(stop_router.router)

# app.mount("/static", StaticFiles(directory="static"), name="static")