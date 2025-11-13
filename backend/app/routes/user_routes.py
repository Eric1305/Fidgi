from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from ..database.db import create_user, get_all_users, get_user_by_clerk_id
from ..utils import authenticate_and_get_user_details
from ..database.models import get_db

router = APIRouter(tags=["Users"])

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)

@router.get("/me")
def get_my_profile(request: Request, db: Session = Depends(get_db)):
    user_details = authenticate_and_get_user_details(request)
    clerk_user_id = user_details.get("user_id")

    user = get_user_by_clerk_id(db, clerk_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user