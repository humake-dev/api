from xmlrpc.client import Boolean

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database import Base

class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    content = relationship("NoticeContent", back_populates="notice", uselist=False)

class NoticeContent(Base):
    __tablename__ = "notice_contents"

    id = Column(Integer, ForeignKey("notices.id"), primary_key=True)
    content = Column(Text, nullable=False)
    notice = relationship("Notice",primaryjoin="Notice.id == foreign(NoticeContent.id)")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    enable = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    picture = relationship("UserPicture", back_populates="user", uselist=False)

class UserPicture(Base):
    __tablename__ = "user_pictures"

    id = Column(Integer, primary_key=True)
    picture_url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User",primaryjoin="User.id == foreign(UserPicture.user_id)")

class Trainer(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    picture = relationship("TrainerPicture", back_populates="trainer", uselist=False)

class TrainerPicture(Base):
    __tablename__ = "admin_pictures"

    id = Column(Integer, primary_key=True)
    picture_url = Column(String, nullable=False)
    admin_id = Column(Integer, ForeignKey("admins.id"))
    trainer = relationship("Trainer",primaryjoin="Trainer.id == foreign(TrainerPicture.admin_id)")

class ExerciseCategory(Base):
    __tablename__ = "exercise_categories"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    picture = relationship("ExerciseCategoryPicture", back_populates="exercise_category", uselist=False)

class ExerciseCategoryPicture(Base):
    __tablename__ = "exercise_category_pictures"

    id = Column(Integer, primary_key=True)
    picture_url = Column(String, nullable=False)
    exercise_category_id = Column(Integer, ForeignKey("exercise_categories.id"))
    exercise_category = relationship("ExerciseCategory",primaryjoin="ExerciseCategory.id == foreign(ExerciseCategoryPicture.exercise_category_id)")

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    exercise_category_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    picture = relationship("ExercisePicture", back_populates="exercise", uselist=False)

class ExercisePicture(Base):
    __tablename__ = "exercise_pictures"

    id = Column(Integer, primary_key=True)
    picture_url = Column(String, nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    exercise = relationship("Exercise",primaryjoin="Exercise.id == foreign(ExercisePicture.exercise_id)")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class ReservationUser(Base):
    __tablename__ = "reservation_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    complete_at = Column(DateTime, nullable=False)
    reservation_id = Column(Integer, ForeignKey("reservations.id"))
    reservation = relationship("Reservation",primaryjoin="Reservation.id == foreign(ReservationUser.reservation_id)")

class Entrance(Base):
    __tablename__ = "entrances"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    in_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
