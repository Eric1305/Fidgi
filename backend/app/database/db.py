from sqlalchemy.orm import Session
from . import models

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