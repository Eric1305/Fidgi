from sqlalchemy.orm import Session
from . import models

# User CRUD operations

def create_user(db: Session, clerk_user_id: str, name: str = None, email: str = None):
    db_user = models.User(clerk_user_id=clerk_user_id, name=name, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_clerk_id(db: Session, clerk_user_id: str):
    return db.query(models.User).filter(models.User.clerk_user_id == clerk_user_id).first()

def get_all_users(db: Session):
    return db.query(models.User).all()

# Item CRUD operations

def create_item(db: Session, name: str, price: float, description: str = None, image: str = None, category: str = None, quantity: int = 0):
    db_item = models.Item(name=name, price=price, description=description, image=image, category=category, quantity=quantity)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all_items(db: Session):
    return db.query(models.Item).all()

def get_item_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def update_item(db: Session, item_id: int, **kwargs):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        return None
    for key, value in kwargs.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# Cart CRUD operations

def add_to_cart(db: Session, user_id: int, item_id: int, quantity: int = 1):
    # Check if item already in cart
    existing = db.query(models.Cart).filter(
        models.Cart.user_id == user_id,
        models.Cart.item_id == item_id
    ).first()
    
    if existing:
        existing.quantity += quantity
        db.commit()
        db.refresh(existing)
        return existing
    
    cart_item = models.Cart(
        user_id=user_id,
        item_id=item_id,
        quantity=quantity
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

def get_user_cart(db: Session, user_id: int):
    return db.query(models.Cart).filter(models.Cart.user_id == user_id).all()

def update_cart_item(db: Session, cart_item_id: int, quantity: int):
    cart_item = db.query(models.Cart).filter(models.Cart.id == cart_item_id).first()
    if cart_item:
        cart_item.quantity = quantity
        db.commit()
        db.refresh(cart_item)
    return cart_item

def remove_from_cart(db: Session, cart_item_id: int):
    cart_item = db.query(models.Cart).filter(models.Cart.id == cart_item_id).first()
    if cart_item:
        db.delete(cart_item)
        db.commit()
        return True
    return False

# Order CRUD operations

def create_order(db: Session, user_id: int, items: list, subtotal: float, discount: float, tax: float, total: float, discount_code: str = None, stripe_payment_id: str = None):
    order = models.Order(
        user_id=user_id,
        subtotal=subtotal,
        discount=discount,
        tax=tax,
        total=total,
        discount_code=discount_code,
        stripe_payment_id=stripe_payment_id,
        status="pending"
    )
    db.add(order)
    db.flush()
    
    for item_data in items:
        order_item = models.OrderItem(
            order_id=order.id,
            item_id=item_data["item_id"],
            name=item_data["name"],
            price=item_data["price"],
            quantity=item_data["quantity"]
        )
        db.add(order_item)
        
        item = get_item_by_id(db, item_data["item_id"])
        if item:
            item.quantity -= item_data["quantity"]
    
    db.query(models.Cart).filter(models.Cart.user_id == user_id).delete()
    
    db.commit()
    db.refresh(order)
    return order

def get_user_orders(db: Session, user_id: int):
    orders = db.query(models.Order).filter(
        models.Order.user_id == user_id
    ).order_by(models.Order.created_at.desc()).all()
    
    result = []
    for order in orders:
        order_items = db.query(models.OrderItem).filter(
            models.OrderItem.order_id == order.id
        ).all()
        
        result.append({
            "id": order.id,
            "subtotal": order.subtotal,
            "discount": order.discount,
            "tax": order.tax,
            "total": order.total,
            "discount_code": order.discount_code,
            "status": order.status,
            "created_at": order.created_at,
            "items": [{
                "item_id": item.item_id,
                "name": item.name,
                "price": item.price,
                "quantity": item.quantity
            } for item in order_items]
        })
    
    return result

def get_order_by_id(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        return None
    
    order_items = db.query(models.OrderItem).filter(
        models.OrderItem.order_id == order.id
    ).all()
    
    return {
        "id": order.id,
        "user_id": order.user_id,
        "subtotal": order.subtotal,
        "discount": order.discount,
        "tax": order.tax,
        "total": order.total,
        "discount_code": order.discount_code,
        "stripe_payment_id": order.stripe_payment_id,
        "status": order.status,
        "created_at": order.created_at,
        "items": [{
            "item_id": item.item_id,
            "name": item.name,
            "price": item.price,
            "quantity": item.quantity
        } for item in order_items]
    }

def get_all_orders(db: Session, sort_by: str = "date", order: str = "desc"):
    from sqlalchemy import desc, asc
    
    query = db.query(models.Order)
    
    if sort_by == "amount":
        query = query.order_by(desc(models.Order.total) if order == "desc" else asc(models.Order.total))
    elif sort_by == "customer":
        query = query.order_by(desc(models.Order.user_id) if order == "desc" else asc(models.Order.user_id))
    else:  # date
        query = query.order_by(desc(models.Order.created_at) if order == "desc" else asc(models.Order.created_at))
    
    orders = query.all()
    
    result = []
    for order in orders:
        user = db.query(models.User).filter(models.User.id == order.user_id).first()
        order_items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order.id).all()
        
        result.append({
            "id": order.id,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            } if user else None,
            "subtotal": order.subtotal,
            "discount": order.discount,
            "tax": order.tax,
            "total": order.total,
            "discount_code": order.discount_code,
            "status": order.status,
            "created_at": order.created_at,
            "items": [{
                "name": item.name,
                "price": item.price,
                "quantity": item.quantity
            } for item in order_items]
        })
    
    return result