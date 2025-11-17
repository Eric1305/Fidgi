from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database.db import (
    get_all_orders,
    get_all_items,
    update_item,
    delete_item,
    create_item,
    get_all_users
)
from ..database.models import get_db
from ..utils import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

# Orders

@router.get("/orders")
def admin_get_all_orders(
    sort_by: str = "date",
    order: str = "desc",
    request: Request = None,
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    orders = get_all_orders(db, sort_by=sort_by, order=order)
    return orders

# Item

class CreateItemRequest(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    image: Optional[str] = None
    category: Optional[str] = None
    quantity: int = 0

class UpdateItemRequest(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    image: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None

@router.post("/items")
def admin_create_item(
    item: CreateItemRequest,
    request: Request = None,
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    new_item = create_item(
        db,
        name=item.name,
        price=item.price,
        description=item.description,
        image=item.image,
        category=item.category,
        quantity=item.quantity
    )
    return {"message": "Item created successfully", "item": new_item}

@router.put("/items/{item_id}")
def admin_update_item(
    item_id: int,
    item: UpdateItemRequest,
    request: Request = None,
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    update_data = {k: v for k, v in item.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    updated_item = update_item(db, item_id, **update_data)
    
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"message": "Item updated successfully", "item": updated_item}

@router.delete("/items/{item_id}")
def admin_delete_item(
    item_id: int,
    request: Request = None,
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    deleted_item = delete_item(db, item_id)
    
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"message": "Item deleted successfully"}

# Users

@router.get("/users")
def admin_get_all_users(
    request: Request = None,
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    users = get_all_users(db)
    return users

# Stats

@router.get("/stats")
def admin_get_stats(
    request: Request = None,
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    from ..database import models
    
    total_orders = db.query(models.Order).count()
    total_revenue = db.query(models.Order).with_entities(
        db.func.sum(models.Order.total)
    ).scalar() or 0.0
    
    total_users = db.query(models.User).count()
    total_items = db.query(models.Item).count()
    
    recent_orders = get_all_orders(db, sort_by="date", order="desc")[:5]
    
    low_stock = db.query(models.Item).filter(models.Item.quantity < 10).all()
    
    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_users": total_users,
        "total_items": total_items,
        "recent_orders": recent_orders,
        "low_stock_items": [{
            "id": item.id,
            "name": item.name,
            "quantity": item.quantity
        } for item in low_stock]
    }
