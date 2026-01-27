from models import Rent, Order, Admin, User, OrderProduct, Product
from sqlalchemy import select, func, cast, Date
from sqlalchemy.orm import Session
from datetime import datetime

def get_rent_list(db: Session, current_user: User | Admin, skip: int = 0, limit: int = 10,  user_id: int | None = None,):
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

    # ⬇️ 여기부터 DB 접근
    stmt = (
        select(
            Rent.id,
            cast(Rent.start_datetime, Date).label("start_date"),
            cast(Rent.end_datetime, Date).label("end_date"),
            Rent.no,
            Product.title.label("product_title"),
        )
        .join(Order, Rent.order_id == Order.id)
        .join(OrderProduct, OrderProduct.order_id == Order.id)
        .join(Product, OrderProduct.product_id == Product.id)
        .where(
            Order.branch_id == current_user.branch_id,
            Order.enable.is_(True),
            Rent.start_datetime <= datetime.now(),
            Rent.end_datetime >= datetime.now(),
        )
        .order_by(Order.id.desc())
    )

    # 🔑 user_id 조건은 단순화
    target_user_id = user_id if isinstance(current_user, Admin) else current_user.id
    stmt = stmt.where(Order.user_id == target_user_id)

    # count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.execute(count_stmt).scalar_one()

    rent_list = (
        db.execute(
            stmt.offset(skip).limit(limit)
        )
        .mappings()
        .all()
    )

    return total, rent_list

def get_rent(db: Session, current_user: User | Admin, id: int):
    rent = db.query(Rent).get(id)
    return rent