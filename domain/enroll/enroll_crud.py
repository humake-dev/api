from models import Enroll, Order, Admin, User, OrderProduct, ProductRelation, Product, EnrollTrainer, Course
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import date

PRIMARY_COURSE_ID = 4

def get_enroll_list(
        db: Session,
        current_user: User | Admin,
        skip: int = 0,
        limit: int = 10,
        user_id: int | None = None,
        primary_only: bool = False,
        current_only: bool = True
    ):
    # 🔐 권한 / 파라미터 검증 먼저
    if isinstance(current_user, Admin):
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin 요청 시 user_id는 필수입니다."
            )
    else:
        if user_id is not None and user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="본인 외 사용자의 데이터는 조회할 수 없습니다."
            )

    today = date.today()

    # ⬇️ 여기부터 DB 접근
    stmt = (
        select(
            Enroll.id,
            Enroll.start_date,
            Enroll.end_date,
            Enroll.quantity,
            Enroll.use_quantity,
            Course.lesson_type.label("lesson_type"),
            Product.title.label("product_title"),
            Admin.name.label("trainer_name"),
        )
        .join(Course, Enroll.course_id == Course.id)
        .join(Order, Enroll.order_id == Order.id)
        .join(OrderProduct, OrderProduct.order_id == Order.id)
        .join(Product, OrderProduct.product_id == Product.id)
        .join(EnrollTrainer, EnrollTrainer.enroll_id == Enroll.id, isouter=True)
        .join(Admin, EnrollTrainer.trainer_id == Admin.id, isouter=True)
        .where(
            Order.branch_id == current_user.branch_id,
            Order.enable.is_(True)
        )
        .order_by(Order.id.desc())
    )

    if primary_only:
        stmt = (
            stmt
            .join(ProductRelation, OrderProduct.product_id == ProductRelation.product_id)
            .where(ProductRelation.product_relation_type_id == PRIMARY_COURSE_ID)
        )

    if current_only:
        stmt = stmt.where(
            Enroll.start_date <= today,
            Enroll.end_date >= today,
        )



    # 🔑 user_id 조건은 단순화
    target_user_id = user_id if isinstance(current_user, Admin) else current_user.id
    stmt = stmt.where(Order.user_id == target_user_id)

    # count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.execute(count_stmt).scalar_one()

    enroll_list = (
        db.execute(
            stmt.offset(skip).limit(limit)
        )
        .mappings()
        .all()
    )

    return total, enroll_list

