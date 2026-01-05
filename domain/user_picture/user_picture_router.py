from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from domain.user_picture import user_picture_schema, user_picture_crud
from starlette import status
from default_func import *
from datetime import datetime
import os
import io
from PIL import Image
from models import UserPicture
import time
import random
import hashlib
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from fastapi import BackgroundTasks


def azure_upload_task(data: bytes, thumb_path: str, orig_name: str, thumb_name: str, branch_id: int):
	"""Background task: upload original bytes and thumb file to Azure under user/<branch_id>/"""
	try:
		load_dotenv()
		fog_provider = os.getenv("FOG_PROVIDER")
		if not (fog_provider and fog_provider.lower() == "azurerm"):
			return

		container_name = os.getenv("FOG_DIRECTORY") or os.getenv("AZURE_CONTAINER") or "humake"
		account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
		access_key = os.getenv("AZURE_STORAGE_ACCESS_KEY")
		if access_key:
			access_key = access_key.strip("'\"")
		if not (account_name and access_key):
			return

		account_url = f"https://{account_name}.blob.core.windows.net"
		client = BlobServiceClient(account_url=account_url, credential=access_key)
		container_client = client.get_container_client(container_name)
		try:
			container_client.create_container()
		except Exception:
			pass

		# upload original bytes
		blob_orig_name = f"user/{branch_id}/{orig_name}"
		try:
			container_client.upload_blob(name=blob_orig_name, data=data, overwrite=True)
		except Exception:
			try:
				from io import BytesIO
				container_client.upload_blob(name=blob_orig_name, data=BytesIO(data), overwrite=True)
			except Exception:
				pass

		# upload thumb file from disk
		blob_thumb_name = f"user/{branch_id}/{thumb_name}"
		try:
			with open(thumb_path, "rb") as thumb_file:
				container_client.upload_blob(name=blob_thumb_name, data=thumb_file, overwrite=True)
		except Exception:
			pass
	except Exception:
		# swallow all to ensure background task never raises to FastAPI internals
		return


router = APIRouter(prefix="/user_pictures", dependencies=[Depends(get_current_user)])


@router.post("", response_model=user_picture_schema.UserPictureCreate)
def upload_user_picture(user_id: int | None = Form(None), picture: UploadFile = File(...), db: Session = Depends(get_db), current_user: User | Admin = Depends(get_current_user), background_tasks: BackgroundTasks = None):
	# determine target user
	if user_id is None:
		user_id = current_user.id
	else:
		# only admin can upload for other users
		if not isinstance(current_user, Admin):
			raise HTTPException(status_code=403, detail="Permission denied")

	# ensure user exists
	target = db.query(User).get(user_id)
	if not target:
		raise HTTPException(status_code=404, detail="user not found")

	# read uploaded bytes and check size
	data = picture.file.read()
	if not data:
		raise HTTPException(status_code=400, detail="Empty file uploaded")

	max_bytes = 5 * 1024 * 1024  # 5 MB
	if len(data) > max_bytes:
		raise HTTPException(status_code=413, detail="File too large (max 5MB)")

	# determine extension and validate
	orig_filename = (picture.filename or "").lower()
	_, ext = os.path.splitext(orig_filename)
	allowed = {".jpg", ".jpeg", ".png"}
	if ext not in allowed:
		# also allow based on content_type fallback
		ct = (picture.content_type or "").lower()
		if ct not in ("image/jpeg", "image/jpg", "image/png"):
			raise HTTPException(status_code=400, detail="Only jpg and png are allowed")

	# pick normalized extension
	if ext in (".jpg", ".jpeg"):
		norm_ext = "jpg"
	else:
		norm_ext = "png"

	# open image and process (center-crop to square, then resize to 200x200)
	try:
		img = Image.open(io.BytesIO(data))
	except Exception:
		raise HTTPException(status_code=400, detail="Invalid image file")

	# crop center square and resize
	img = img.convert("RGBA")
	width, height = img.size
	min_side = min(width, height)
	left = (width - min_side) // 2
	top = (height - min_side) // 2
	right = left + min_side
	bottom = top + min_side
	img = img.crop((left, top, right, bottom))
	img = img.resize((200, 200), Image.LANCZOS)

	# prepare upload directory
	upload_dir = os.path.join(os.getcwd(), "static", "user", current_user.branch_id.__str__())
	os.makedirs(upload_dir, exist_ok=True)

	# generate uniqid()-like filename (based on microtime hex + random entropy)
	# generate a compact 13-char filename (hex) to mimic PHP uniqid length
	def uniq13() -> str:
		mt = int(time.time() * 1_000_000)
		# use sha1 over time + random bits and take first 13 hex chars
		src = f"{mt}{random.getrandbits(64)}{random.random()}"
		return hashlib.sha1(src.encode()).hexdigest()[:13]

	uniq = uniq13()
	orig_name = f"{uniq}.{norm_ext}"
	thumb_name = f"medium_thumb_{uniq}.{norm_ext}"
	file_path = os.path.join(upload_dir, thumb_name)

	# save original uploaded file locally with its original filename (overwrite if exists)
	orig_uploaded_basename = os.path.basename(picture.filename) if (picture.filename) else orig_name
	orig_local_path = os.path.join(upload_dir, orig_uploaded_basename)
	try:
		with open(orig_local_path, "wb") as f:
			f.write(data)
	except Exception:
		# ignore local save errors; continue
		pass

	# also save a copy of the original bytes using the generated uuid filename
	uuid_local_path = os.path.join(upload_dir, orig_name)
	try:
		with open(uuid_local_path, "wb") as f:
			f.write(data)
	except Exception:
		# ignore local save errors; continue
		pass

	# remove previous file if exists and different
	existing = db.query(UserPicture).filter(UserPicture.user_id == user_id).first()
	if existing and existing.picture_url:
		# existing.picture_url may be full path or just filename
		if existing.picture_url.startswith("/") or existing.picture_url.startswith("static"):
			old_path = os.path.join(os.getcwd(), existing.picture_url.lstrip("/"))
		else:
			old_path = os.path.join(upload_dir, existing.picture_url)
		if os.path.exists(old_path) and os.path.abspath(old_path) != os.path.abspath(file_path):
			try:
				os.remove(old_path)
			except Exception:
				pass

	# save image according to extension
	if norm_ext == "jpg":
		# paste onto white background to remove alpha channel then save jpeg
		background = Image.new("RGB", (200, 200), (255, 255, 255))
		background.paste(img, mask=img.split()[3])
		background.save(file_path, format="JPEG", quality=85, optimize=True)
	else:
		# save png
		img.save(file_path, format="PNG", optimize=True)

	# store the UUID-named original filename in DB (without the "medium_thumb_" prefix)
	picture_url = orig_name

	# schedule Azure upload in background (do not block response)
	try:
		if background_tasks is not None:
			background_tasks.add_task(azure_upload_task, data, file_path, orig_name, thumb_name, current_user.branch_id)
	except Exception:
		# scheduling failed — ignore and continue
		pass

	pic = user_picture_crud.set_user_picture(db, user_id, picture_url)

	return {"id": pic.id, "picture_url": pic.picture_url}
