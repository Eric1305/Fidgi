from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user_model import User

from ..utils.auth import get_clerk_user 

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def get_my_profile(clerk_user: dict = Depends(get_clerk_user), db: Session = Depends(get_db)):

    clerk_id = clerk_user.get("user_id")

    user = db.query(User).filter(User.clerk_user_id == clerk_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User profile not synced. Please log out and log in again.")

    return user

@router.get("/all")
def get_all_users(clerk_user: dict = Depends(get_clerk_user), db: Session = Depends(get_db)):
    
    print(f"User {clerk_user.get('user_id')} is requesting all users.")
    return db.query(User).all()