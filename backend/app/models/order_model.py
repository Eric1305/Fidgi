from sqlalchemy import Column, Integer, String
from ..database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    status = Column(String, nullable=False, default="pending")
    shipping_address = Column(String, nullable=True)
    billing_address = Column(String, nullable=True)
    