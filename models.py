from sqlalchemy import Column, Integer, Float, String, Text, Date, DateTime, ForeignKey, Boolean, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from enum import Enum
from sqlalchemy.ext.associationproxy import association_proxy

class CounselQuestionCourse(str, Enum):
    default = "default"
    pt = "pt"

class AdminStatus(str, Enum):
    H = "H"
    R = "R"
    L = "L"

class UserDeviceOS(str, Enum):
    android = "android"
    ios = "ios"


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, nullable=False)
    uid = Column(String, nullable=False)    
    name = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)    
    is_trainer = Column(Boolean, nullable=False)
    status = Column(SqlEnum(AdminStatus), nullable=False, default=AdminStatus.H)
    enable = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    picture = relationship("AdminPicture", back_populates="admin", uselist=False)


# Trainer는 단순히 편의용 alias + Query
Trainer = Admin

class AdminPicture(Base):
    __tablename__ = "admin_pictures"

    id = Column(Integer, primary_key=True)
    picture_url = Column(String, nullable=False)
    admin_id = Column(Integer, ForeignKey("admins.id"))
    admin = relationship("Admin",primaryjoin="Admin.id == foreign(AdminPicture.admin_id)")

TrainerPicture = AdminPicture 


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

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    app_title_color = Column(String, nullable=False)
    app_notice_color = Column(String, nullable=False)
    enable = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    picture = relationship(
        "BranchPicture",
        back_populates="branch",
        uselist=False
    )

class BranchPicture(Base):
    __tablename__ = "branch_pictures"

    id = Column(Integer, primary_key=True)
    picture_url = Column(String, nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id"))
    branch = relationship(
        "Branch",
        back_populates="picture"
    )

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    enable = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    picture = relationship("UserPicture", back_populates="user", uselist=False)
    access_card = relationship("UserAccessCard", back_populates="user", uselist=False)
    user_height = relationship("UserHeight", back_populates="user", uselist=False)
    user_weight = relationship("UserWeight", back_populates="user", order_by="desc(UserWeight.id)", uselist=False)

    user_trainer = relationship("UserTrainer", back_populates="user", uselist=False)
    trainer = association_proxy("user_trainer", "trainer")

class UserAccessCard(Base):
    __tablename__ = "user_access_cards"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    card_no = Column(String, nullable=False)
    user = relationship("User",primaryjoin="User.id == foreign(UserAccessCard.user_id)")

class UserPicture(Base):
    __tablename__ = "user_pictures"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    picture_url = Column(String, nullable=False)
    user = relationship("User",primaryjoin="User.id == foreign(UserPicture.user_id)")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)    

class UserTrainer(Base):
    __tablename__ = "user_trainers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trainer_id = Column(Integer, ForeignKey("admins.id"))

    user = relationship("User", back_populates="user_trainer")
    trainer = relationship("Admin")

class UserHeight(Base):
    __tablename__ = "user_heights"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    height = Column(Float, nullable=False)
    user = relationship("User",primaryjoin="User.id == foreign(UserHeight.user_id)")

class UserWeight(Base):
    __tablename__ = "user_weights"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    weight = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    user = relationship("User",primaryjoin="User.id == foreign(UserWeight.user_id)")

class UserDevice(Base):
    __tablename__ = "user_devices"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    os = Column(SqlEnum(UserDeviceOS), nullable=False)
    token = Column(String, nullable=False)
    enable = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)


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
    branch_id = Column(Integer, nullable=False)    
    manager_id = Column(Integer, ForeignKey("admins.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    enable = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    trainer = relationship("Admin",primaryjoin="Admin.id == foreign(Reservation.manager_id)")

class ReservationUser(Base):
    __tablename__ = "reservation_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    complete = Column(Integer, primary_key=True)
    complete_at = Column(DateTime, nullable=False)
    reservation_id = Column(Integer, ForeignKey("reservations.id"))
    reservation = relationship("Reservation",primaryjoin="Reservation.id == foreign(ReservationUser.reservation_id)")

class Entrance(Base):
    __tablename__ = "entrances"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    in_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    user = relationship("User",primaryjoin="User.id == foreign(Entrance.user_id)")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    enable = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    content = relationship("MessageContent", back_populates="message", uselist=False)

class MessageUser(Base):
    __tablename__ = "message_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    display = Column(Boolean, nullable=False)
    readtime = Column(DateTime, nullable=False)
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
    enable = Column(Boolean, default=True, nullable=False)
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
    complete = Column(Boolean, default=False)
    enable = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer,unique=True, nullable=False)
    user_id = Column(Integer,unique=True, nullable=False)
    enable = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class Enroll(Base):
    __tablename__ = "enrolls"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    course_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    use_quantity = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

class Rent(Base):
    __tablename__ = "rents"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    facility_id = Column(Integer, nullable=False)
    no = Column(Integer, nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)

class OrderProduct(Base):
    __tablename__ = "order_products"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

class ProductRelation(Base):
    __tablename__ = "product_relations"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    product_relation_type_id = Column(Integer)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

class EnrollTrainer(Base):
    __tablename__ = "enroll_trainers"

    id = Column(Integer, primary_key=True)
    enroll_id = Column(Integer, ForeignKey("enrolls.id"))
    trainer_id = Column(Integer, ForeignKey("admins.id"))

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    lesson_type = Column(Integer, nullable=False)