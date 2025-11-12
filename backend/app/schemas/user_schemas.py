from pydantic import BaseModel, EmailStr

# Base properties that are shared
class UserBase(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None

# Properties used internally when creating a user
class UserCreate(UserBase):
    clerk_user_id: str

# Properties to return to the client (from your DB)
class User(UserBase):
    id: int

    class Config:
        orm_mode = True 