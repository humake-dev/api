from models import Enroll, Order, Admin, User, OrderProduct, ProductRelation
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
):
    query = (
        db.query(Enroll)
        .join(Order)
        .filter(
            Order.branch_id == current_user.branch_id,
            Order.enable == True,
            Enroll.start_date <= date.today(),
            Enroll.end_date >= date.today(),
        )
        .order_by(Order.id.desc())
    )

    if primary_only:
        query = (
            query
            .join(OrderProduct, OrderProduct.order_id == Order.id )
            .join(ProductRelation, OrderProduct.product_id == ProductRelation.product_id)
            .filter(ProductRelation.product_relation_type_id == PRIMARY_COURSE_ID)
        )

    if isinstance(current_user, Admin):
        if user_id:
            query = query.filter(Order.user_id == user_id)
    else:
        query = query.filter(Order.user_id == current_user.id)

    total = query.count()
    enroll_list = query.offset(skip).limit(limit).all()

    return total, enroll_list

