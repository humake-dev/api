from models import UserDevice, User
from sqlalchemy.orm import Session
from domain.user_device import user_device_schema
from sqlalchemy.dialects.mysql import insert

def set_user_device(db: Session, current_user: User, user_device_data: user_device_schema.UserDeviceCreate):
    stmt = insert(UserDevice).values(
        user_id=current_user.id,
        os=user_device_data.os,
        token=user_device_data.token
    )

    update_dict = {
        'token': user_device_data.token
    }

    stmt = stmt.on_duplicate_key_update(**update_dict)

    result = db.execute(stmt)
    db.commit()

    # result.inserted_primary_key[0]로 id를 가져올 수 있음 (필요하면)
    return result.lastrowid  # 또는 inserted_primary_key[0]