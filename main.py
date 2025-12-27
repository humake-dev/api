from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware



from domain.admin import admin_router
from domain.branch import branch_router
from domain.notice import notice_router
from domain.user import user_router
from domain.user import users_router
from domain.user_picture import user_picture_router
from domain.trainer import trainer_router
from domain.exercise import exercise_router
from domain.exercise_category import exercise_category_router
from domain.reservation import reservation_router
from domain.entrance import entrance_router
from domain.message import message_router
from domain.counsel import counsel_router
from domain.stop import stop_router
from domain.user_device import user_device_router
from domain.user_height import user_height_router
from domain.user_weight import user_weight_router
from domain.enroll import enroll_router
from domain.rent import rent_router


app = FastAPI()

# FastAPI 세션 이름 변경 (중요!)
app.add_middleware(
    SessionMiddleware,
    secret_key="humake_api_is_good",
    session_cookie="fastapi_session"
)

origins = [
    "http://127.0.0.1:5173",  # 또는
    #"http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(admin_router.router)
app.include_router(notice_router.router)
app.include_router(branch_router.router)
app.include_router(users_router.router)
app.include_router(user_router.router)
app.include_router(user_picture_router.router)
app.include_router(user_device_router.router)
app.include_router(user_height_router.router)
app.include_router(user_weight_router.router)
app.include_router(trainer_router.router)
app.include_router(exercise_router.router)
app.include_router(exercise_category_router.router)
app.include_router(reservation_router.router)
app.include_router(entrance_router.router)
app.include_router(message_router.router)
app.include_router(counsel_router.router)
app.include_router(stop_router.router)
app.include_router(enroll_router.router)
app.include_router(rent_router.router)


app.mount("/static", StaticFiles(directory="static"), name="static")