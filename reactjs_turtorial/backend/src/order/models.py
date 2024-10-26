from database import Base
from sqlalchemy import Integer, Column,TIMESTAMP, text, ForeignKey, DECIMAL, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func 

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_amount = Column(DECIMAL, nullable=False)
    order_date = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=func.now())
    
    user = relationship("User", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order", cascade="all, delete")
    
class OrderDetail(Base):
    __tablename__ = 'order_detail'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product_name = Column(String(255), nullable=False)
    product_image= Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=func.now())
    
    order = relationship("Order", back_populates="order_details")
    product = relationship("Product", back_populates="order_details")