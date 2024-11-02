# inventory_service/models.py
from sqlalchemy import Column, Integer, String
from base import Base

class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, unique=True)
    quantity = Column(Integer)
