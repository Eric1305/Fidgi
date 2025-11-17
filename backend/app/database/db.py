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
        # Update quantity
        existing.quantity += quantity
        db.commit()
        db.refresh(existing)
        return existing
    
    # Create new cart item
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