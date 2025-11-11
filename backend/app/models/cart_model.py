from sqlalchemy import Column, Integer, String
from ..database import Base

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    added_at = Column(String, nullable=False)
    
    