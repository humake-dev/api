
from sqlalchemy.orm import Session
from models import UserPicture
from datetime import datetime


def set_user_picture(db: Session, user_id: int, picture_url: str):
	"""Insert or update UserPicture for given user_id. Returns the UserPicture instance."""
	existing = db.query(UserPicture).filter(UserPicture.user_id == user_id).first()
	if existing:
		existing.picture_url = picture_url
		existing.updated_at = datetime.utcnow()
		db.commit()
		db.refresh(existing)
		return existing

	now = datetime.utcnow()
	pic = UserPicture(user_id=user_id, picture_url=picture_url, created_at=now, updated_at=now)
	db.add(pic)
	db.commit()
	db.refresh(pic)
	return pic
