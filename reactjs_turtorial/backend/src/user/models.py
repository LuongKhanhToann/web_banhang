from sqlalchemy import Column, Integer, String, TIMESTAMP, text, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    username = Column(String(255), index=True, nullable=False)
    phone_number = Column(String(255), index=True, nullable=False)
    role = Column(String(255), index=True, nullable=False)
    wallet_balance = Column(DECIMAL, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=func.now())
    
    orders = relationship("Order", back_populates='user', cascade="all, delete")
    transactions = relationship("Transaction", back_populates='user', cascade="all, delete")
    
class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    old_amount = Column(DECIMAL, default=0, nullable=False)
    new_amount = Column(DECIMAL, default=0, nullable=False)
    total_amount = Column(DECIMAL, default=0, nullable=False)
    transaction_type = Column(String(255), nullable=False)
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),onupdate=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=func.now())
    
    user = relationship("User", back_populates='transactions')
    