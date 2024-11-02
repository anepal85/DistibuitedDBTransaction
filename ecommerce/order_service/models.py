# order_service/models.py
from sqlalchemy import Column, Integer, ForeignKey, String
from base import Base

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    status = Column(String)
