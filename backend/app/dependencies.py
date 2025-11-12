import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from dotenv import load_dotenv

from .database import get_db
from .models import user_model
from .schemas import user_schemas

load_dotenv()

CLERK_PEM_PUBLIC_KEY = os.environ.get("CLERK_PEM_PUBLIC_KEY")

if not CLERK_PEM_PUBLIC_KEY:
    raise EnvironmentError("CLERK_PEM_PUBLIC_KEY not found in environment variables")

http_bearer_scheme = HTTPBearer()

def get_current_user(auth: HTTPAuthorizationCredentials = Depends(http_bearer_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = auth.credentials
        payload = jwt.decode(
            token,
            CLERK_PEM_PUBLIC_KEY,
            algorithms=["RS256"],
        )
        clerk_user_id: str = payload.get("sub")
        if clerk_user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    db_user = db.query(user_model.User).filter(user_model.User.clerk_user_id == clerk_user_id).first()
    
    if db_user is None:
        
        # NOTE: You MUST configure your Clerk JWT Template to include these
        email = payload.get("email") 
        first_name = payload.get("first_name")
        last_name = payload.get("last_name")

        if email is None:
            # This will fail if the email isn't in the token
            raise HTTPException(400, "Email not found in token payload, check Clerk JWT Template")

        user_to_create = user_schemas.UserCreate(
            clerk_user_id=clerk_user_id,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        db_user = user_model.User(**user_to_create.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    return db_user