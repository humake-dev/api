from fastapi import  Request, HTTPException
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

SECRET_KEY = "awerigkpawegikp23k1233sdaglpaw!@E$a"
serializer = URLSafeTimedSerializer(SECRET_KEY)
SESSION_COOKIE_NAME='humake_api'

def get_session(request: Request):
    session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
    if not session_cookie:
        raise HTTPException(status_code= 401, detail="No Auth")  # 404 응답 반환

    try:
        return serializer.loads(session_cookie, max_age=3600)  # 세션 유효시간: 1시간
    except SignatureExpired:
        raise HTTPException(status_code= 401, detail="No Auth")  # 만료된 세션 → 404 반환
    except Exception:
        raise HTTPException(status_code=401, detail="No Auth")  # 기타 예외는 400 에러
    

def get_admin_session(request: Request):
    session = get_session(request)
    if not session.get("admin_id"):
        raise HTTPException(status_code=401, detail="No Auth")
    return session    