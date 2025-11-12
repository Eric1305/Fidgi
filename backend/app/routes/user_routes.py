from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas import user_schemas
from ..models import user_model
from ..database import get_db
from ..dependencies import get_current_user # <-- Import your new dependency

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

@router.get("/me", response_model=user_schemas.User)
def read_users_me(current_user: user_model.User = Depends(get_current_user)):
    """
    Get the profile for the currently logged-in user.
    If the user doesn't exist in the database, they will be
    created "just-in-time".
    """
    return current_user

@router.put("/me", response_model=user_schemas.User)
def update_users_me(
    user_updates: user_schemas.UserBase, # Use UserBase (email, first, last)
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the current user's app-specific profile information
    (e.g., first_name, last_name).
    """
    # Get the update data from the request
    update_data = user_updates.dict(exclude_unset=True)
    
    # Update the user object
    for key, value in update_data.items():
        setattr(current_user, key, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user