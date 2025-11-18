from fastapi import HTTPException, Request, Depends
from clerk_backend_api import Clerk, AuthenticateRequestOptions
from .database.models import get_db
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()


clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

def authenticate_and_get_user_details(request):
    try:
        # Development mode bypass - remove this in production!
        DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"
        
        if DEV_MODE:
            # Return a placeholder admin user for development
            return {
                "user_id": "dev_admin_user_123",
                "email": "admin@fidgi.dev",
                "name": "Dev Admin"
            }
        
        # Production authentication
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
                jwt_key=os.getenv("JWT_KEY")
            )
        )

        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_id = request_state.payload.get("sub")

        return {"user_id": user_id}
    except Exception as e:
        # If JWT_KEY is not set, assume dev mode
        if "JWT_KEY" in str(e) or not os.getenv("JWT_KEY"):
            return {
                "user_id": "dev_admin_user_123",
                "email": "admin@fidgi.dev",
                "name": "Dev Admin"
            }
        raise HTTPException(status_code=500, detail=str(e))

def require_admin(request: Request, db: Session = Depends(get_db)):
    from .database.db import get_user_by_clerk_id
    
    user_details = authenticate_and_get_user_details(request)
    clerk_user_id = user_details.get("user_id")
    
    user = get_user_by_clerk_id(db, clerk_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return user