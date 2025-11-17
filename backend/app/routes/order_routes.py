from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..database.db import (
    get_user_by_clerk_id,
    get_user_cart,
    get_item_by_id,
    create_order,
    get_user_orders,
    get_all_orders,
    get_order_by_id
)
from ..database.models import get_db
from ..utils import authenticate_and_get_user_details

router = APIRouter(prefix="/orders", tags=["Orders"])

class CreateOrderRequest(BaseModel):
    discount_code: Optional[str] = None
    stripe_payment_id: str

class OrderItemResponse(BaseModel):
    item_id: int
    name: str
    price: float
    quantity: int
    subtotal: float

class OrderResponse(BaseModel):
    id: int
    user_id: int
    subtotal: float
    discount: float
    tax: float
    total: float
    discount_code: Optional[str]
    stripe_payment_id: str
    status: str
    created_at: datetime
    items: List[OrderItemResponse]
    
@router.post("/")
def create_new_order(
    order_request: CreateOrderRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    user_details = authenticate_and_get_user_details(request)
    clerk_user_id = user_details.get("user_id")
    
    user = get_user_by_clerk_id(db, clerk_user_id)
    if not user:
        from ..database.db import create_user
        user = create_user(db, clerk_user_id)
    
    cart_items = get_user_cart(db, user.id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    order_items = []
    subtotal = 0.0
    
    for cart_item in cart_items:
        item = get_item_by_id(db, cart_item.item_id)
        
        if not item:
            raise HTTPException(
                status_code=404, 
                detail=f"Item {cart_item.item_id} not found"
            )
        
        if item.quantity < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {item.name}. Only {item.quantity} available"
            )
        
        item_total = item.price * cart_item.quantity
        subtotal += item_total
        
        order_items.append({
            "item_id": item.id,
            "name": item.name,
            "price": item.price,
            "quantity": cart_item.quantity
        })
    
    discount_amount = 0.0
    if order_request.discount_code:
        from ..database.models import discountCode
        discount = db.query(discountCode).filter(
            discountCode.code == order_request.discount_code.upper()
        ).first()
        
        if discount:
            discount_amount = subtotal * (discount.discount_percentage / 100)
    
    after_discount = subtotal - discount_amount
    tax = after_discount * 0.0825
    total = after_discount + tax
    
    order = create_order(
        db,
        user_id=user.id,
        items=order_items,
        subtotal=subtotal,
        discount=discount_amount,
        tax=tax,
        total=total,
        discount_code=order_request.discount_code,
        stripe_payment_id=order_request.stripe_payment_id
    )
    
    return {
        "message": "Order created successfully",
        "order_id": order.id,
        "total": total
    }

@router.get("/")
def get_my_orders(
    request: Request,
    db: Session = Depends(get_db)
):
    user_details = authenticate_and_get_user_details(request)
    clerk_user_id = user_details.get("user_id")
    
    user = get_user_by_clerk_id(db, clerk_user_id)
    if not user:
        return []
    
    orders = get_user_orders(db, user.id)
    return orders

@router.get("/{order_id}")
def get_order_details(
    order_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user_details = authenticate_and_get_user_details(request)
    clerk_user_id = user_details.get("user_id")
    
    user = get_user_by_clerk_id(db, clerk_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return order

# Admin routes
@router.get("/admin/all")
def get_all_orders_admin(
    request: Request,
    db: Session = Depends(get_db),
    sort_by: Optional[str] = "date",
    order: Optional[str] = "desc"
):
    user_details = authenticate_and_get_user_details(request)
    
    orders = get_all_orders(db, sort_by=sort_by, order=order)
    return orders

@router.put("/{order_id}/status")
def update_order_status(
    order_id: int,
    status: str,
    request: Request,
    db: Session = Depends(get_db)
):
    user_details = authenticate_and_get_user_details(request)
    
    from ..database.models import Order
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    db.commit()
    db.refresh(order)
    
    return {"message": "Order status updated", "order": order}