from fastapi import Depends, HTTPException
from clerk_fastapi import get_session

def get_clerk_user(session: dict = Depends(get_session)):
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if "user_id" not in session:
        raise HTTPException(status_code=401, detail="Invalid session, user_id missing.")

    return session