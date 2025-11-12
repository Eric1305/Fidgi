import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from dotenv import load_dotenv

# Import your DB session, models, and schemas
from .database import get_db
from .models import user_model
from .schemas import user_schemas

load_dotenv()

# --- IMPORTANT ---
# Go to your Clerk Dashboard -> API Keys -> Advanced
# Grab the -----BEGIN PUBLIC KEY-----... part and put it in your .env.local
# Make sure to wrap it in quotes and replace newlines with \n
# CLERK_PEM_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\nMI...[rest of key]...AB\n-----END PUBLIC KEY-----"
CLERK_PEM_PUBLIC_KEY = os.environ.get("CLERK_PEM_PUBLIC_KEY")

if not CLERK_PEM_PUBLIC_KEY:
    raise EnvironmentError("CLERK_PEM_PUBLIC_KEY not found in environment variables")

# This tells FastAPI to look for a "Bearer" token in the Authorization header
http_bearer_scheme = HTTPBearer()

def get_current_user(auth: HTTPAuthorizationCredentials = Depends(http_bearer_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = auth.credentials
        # 1. Validate the token using Clerk's public key
        payload = jwt.decode(
            token,
            CLERK_PEM_PUBLIC_KEY,
            algorithms=["RS256"],
            # You may need to add audience/issuer validation depending on your settings
        )
        clerk_user_id: str = payload.get("sub") # "sub" is the standard JWT claim for user ID
        if clerk_user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    # 2. Check if user exists in YOUR database
    db_user = db.query(user_model.User).filter(user_model.User.clerk_user_id == clerk_user_id).first()
    
    # 3. This is the "Just-in-Time" (JIT) provisioning
    if db_user is None:
        # User is valid in Clerk, but not in our DB. Let's create them.
        
        # NOTE: You MUST configure your Clerk JWT Template to include these
        email = payload.get("email") 
        first_name = payload.get("first_name")
        last_name = payload.get("last_name")

        if email is None:
            # This will fail if the email isn't in the token
            raise HTTPException(400, "Email not found in token payload, check Clerk JWT Template")

        # Create the user in your database
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

    # 4. Return the user from YOUR database
    return db_user