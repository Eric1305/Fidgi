from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.order_model import Order

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/")
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@router.post("/")
def create_order(user_id: int, item_id: int, quantity: int, db: Session = Depends(get_db)):
    new_order = Order(
        user_id=user_id,
        item_id=item_id,
        quantity=quantity
    )

    db.add(new_order)
    db.commit() 
    db.refresh(new_order)

    return {"message": "Order created", "id": new_order.id}

@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()

    return {"message": "Order deleted"}

@router.put("/{order_id}")
def update_order(order_id: int, quantity: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.quantity = quantity
    db.commit()
    db.refresh(order)

    return {"message": "Order updated", "order": order}

@router.get("/user/{user_id}")
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders

@router.get("/item/{item_id}")
def get_orders_by_item(item_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.item_id == item_id).all()
    return orders




