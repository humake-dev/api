from xmlrpc.client import Boolean

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from enum import Enum

class CounselQuestionCourse(str, Enum):
    default = "default"
    pt = "pt"

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

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    content = relationship("MessageContent", back_populates="message", uselist=False)

class MessageUser(Base):
    __tablename__ = "message_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    display = Column(Boolean, nullable=False)
    message_id = Column(Integer, ForeignKey("messages.id"))
    message = relationship("Message",primaryjoin="Message.id == foreign(MessageUser.message_id)")

class MessageContent(Base):
    __tablename__ = "message_contents"

    id = Column(Integer, ForeignKey("messages.id"), primary_key=True)
    content = Column(Text, nullable=False)
    message = relationship("Message",primaryjoin="Message.id == foreign(MessageContent.id)")

class Counsel(Base):
    __tablename__ = "counsels"

    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    execute_date = Column(DateTime, nullable=False)
    question_course = Column(SqlEnum(CounselQuestionCourse), nullable=False, default=CounselQuestionCourse.default)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    content = relationship("CounselContent", back_populates="counsel", uselist=False)

class CounselContent(Base):
    __tablename__ = "counsel_contents"

    id = Column(Integer, ForeignKey("counsels.id"), primary_key=True)
    content = Column(Text, nullable=False)
    counsel = relationship("Counsel",primaryjoin="Counsel.id == foreign(CounselContent.id)")

class CounselUser(Base):
    __tablename__ = "counsel_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    display = Column(Boolean, nullable=False, default=True)
    counsel_id = Column(Integer, ForeignKey("counsels.id"))
    counsel = relationship("Counsel",primaryjoin="Counsel.id == foreign(CounselUser.counsel_id)")

class Stop(Base):
    __tablename__ = "user_stop_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    stop_start_date = Column(DateTime, nullable=False)
    stop_end_date = Column(DateTime, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)