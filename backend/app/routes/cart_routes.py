from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database.db import (
    create_user,
    get_item_by_id,
    get_user_by_clerk_id,
    add_to_cart,
    get_user_cart,
    update_cart_item,
    remove_from_cart
)
from ..database.models import get_db
from ..utils import authenticate_and_get_user_details

router = APIRouter(prefix="/cart", tags=["Cart"])

class AddToCartRequest(BaseModel):
    item_id: int
    quantity: int = 1

class UpdateCartRequest(BaseModel):
    quantity: int

@router.post("/items")
def add_item_to_cart(
    cart_request: AddToCartRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Add item to cart - checks stock availability"""
    user_details = authenticate_and_get_user_details(request)
    clerk_user_id = user_details.get("user_id")
    
    # Get user from database
    user = get_user_by_clerk_id(db, clerk_user_id)
    if not user:
        user = create_user(db, clerk_user_id, name="User", email="")
    
    # Check if item exists
    item = get_item_by_id(db, cart_request.item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check stock availability
    if item.quantity < cart_request.quantity:
        raise HTTPException(
            status_code=400, 
            detail=f"Only {item.quantity} items available in stock"
        )
    
    if item.quantity == 0:
        raise HTTPException(status_code=400, detail="Item out of stock")
    
    # Add to cart
    cart_item = add_to_cart(db, user.id, cart_request.item_id, cart_request.quantity)
    
    return {
        "message": "Item added to cart",
        "cart_item": cart_item
    }

@router.get("/")
def get_cart(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get user's cart with item details"""
    user_details = authenticate_and_get_user_details(request)
    clerk_user_id = user_details.get("user_id")
    
    user = get_user_by_clerk_id(db, clerk_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    cart_items = get_user_cart(db, user.id)
    
    # Add item details and stock check to each cart item
    cart_with_details = []
    for cart_item in cart_items:
        item = get_item_by_id(db, cart_item.item_id)
        
        # Check if item is still in stock
        in_stock = item.quantity >= cart_item.quantity
        
        cart_with_details.append({
            "id": cart_item.id,
            "item_id": cart_item.item_id,
            "quantity": cart_item.quantity,
            "item": {
                "name": item.name,
                "price": item.price,
                "image": item.image,
                "available_quantity": item.quantity
            },
            "in_stock": in_stock,
            "max_available": item.quantity
        })
    
    return cart_with_details

@router.put("/items/{cart_item_id}")
def update_cart_quantity(
    cart_item_id: int,
    cart_update: UpdateCartRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Update cart item quantity - checks stock"""
    user_details = authenticate_and_get_user_details(request)
    
    # Get cart item and verify ownership
    cart_item = db.query(models.Cart).filter(models.Cart.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Check stock
    item = get_item_by_id(db, cart_item.item_id)
    if item.quantity < cart_update.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Only {item.quantity} items available in stock"
        )
    
    # Update quantity
    updated_cart_item = update_cart_item(db, cart_item_id, cart_update.quantity)
    
    return {"message": "Cart updated", "cart_item": updated_cart_item}

@router.delete("/items/{cart_item_id}")
def remove_item_from_cart(
    cart_item_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    user_details = authenticate_and_get_user_details(request)
    
    removed = remove_from_cart(db, cart_item_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    return {"message": "Item removed from cart"}