from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker


# MySQL 접속 정보 설정
DATABASE_URL = "mysql+mysqldb://humake:humake1!@localhost/humake_development"


# 엔진 생성
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

