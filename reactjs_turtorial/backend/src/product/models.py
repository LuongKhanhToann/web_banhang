from database import Base
from sqlalchemy import Column, String, Integer, Double, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    image = Column(String(255), nullable=False)
    price = Column(Double, index=True, nullable=False)
    discount_price = Column(Double, index=True)
    quantity = Column(Integer)
    description = Column(String(255), nullable=False)
    supplier = Column(String(255), index=True, nullable=False)
    group_id = Column(Integer, ForeignKey('product_group.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('product_category.id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=func.now())
    
    product_category = relationship("ProductCategory", back_populates="products")
    product_group = relationship("ProductGroup", back_populates="products")
    order_details = relationship("OrderDetail", back_populates="product", cascade="all, delete")


class ProductCategory(Base):
    __tablename__ = 'product_category'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, unique=True)
    group_id = Column(Integer, ForeignKey('product_group.id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=func.now())
    
    products = relationship("Product", back_populates="product_category", cascade="all, delete")
    product_group = relationship("ProductGroup", back_populates="product_categories")
    
    

class ProductGroup(Base):
    __tablename__ = 'product_group'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=func.now())  
    
    products = relationship("Product", back_populates="product_group", cascade="all, delete")
    product_categories = relationship("ProductCategory", back_populates="product_group", cascade="all, delete")
     