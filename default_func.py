from fastapi import  Request, HTTPException

def get_current_user(request: Request):
    """모든 요청에서 세션을 검사하는 함수"""
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="no_auth")
    return user_id
