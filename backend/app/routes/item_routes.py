from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database.db import (
    create_item, 
    get_all_items, 
    get_item_by_id, 
    update_item, 
    delete_item
)
from ..database.models import get_db
from ..utils import authenticate_and_get_user_details

router = APIRouter(prefix="/items", tags=["Items"])

# Pydantic models for request/response
class ItemCreate(BaseModel):
    name: str
    price: float
    description: str = None
    image: str = None
    category: str = None
    quantity: int = 0

class ItemUpdate(BaseModel):
    name: str = None
    price: float = None
    description: str = None
    image: str = None
    category: str = None
    quantity: int = None

# Public routes
@router.get("/")
def list_items(db: Session = Depends(get_db)):
    return get_all_items(db)

@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Protected routes (require authentication)
@router.post("/")
def create_new_item(
    item: ItemCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    authenticate_and_get_user_details(request)  # Just check auth for now
    return create_item(
        db,
        name=item.name,
        price=item.price,
        description=item.description,
        image=item.image,
        category=item.category,
        quantity=item.quantity
    )

@router.put("/{item_id}")
def update_existing_item(
    item_id: int,
    item: ItemUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    authenticate_and_get_user_details(request)
    
    # Filter out None values
    update_data = {k: v for k, v in item.dict().items() if v is not None}
    
    updated_item = update_item(db, item_id, **update_data)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/{item_id}")
def delete_existing_item(
    item_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    authenticate_and_get_user_details(request)
    
    deleted_item = delete_item(db, item_id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
