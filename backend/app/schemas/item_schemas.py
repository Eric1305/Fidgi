from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int = 0

class ItemRead(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    stock: int

    class Config:
        from_attributes = True
