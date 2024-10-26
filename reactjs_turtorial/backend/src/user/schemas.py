from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime
from decimal import Decimal
from order import schemas

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"
    EMPLOYEE = "EMPLOYEE"
    
class TransactionType(str, Enum):
    WITHDRAW = "WITHDRAW"   
    DEPOSIT = "DEPOSIT"
    
class UserBase(BaseModel):
    email: str
    password: str
        
class UserCreate(UserBase):
    username: str
    phone_number: str
    role: str
    wallet_balance: Decimal = 0.0
        
class UserUpdate(UserBase):
    email: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    wallet_balance: Optional[Decimal] = None
    updated_at: datetime
    role: Optional[str] = None
        
class UserLogin(UserBase):
    email: str
    password: str
    
class UserChangePassword(UserBase):
    new_password: str
        
class WalletCharge(BaseModel):
    amount: Decimal

# transaction schemas
class TransactionBase(BaseModel):
    old_amount: Decimal
    new_amount: Decimal
    total_amount: Optional[Decimal] = 0
    transaction_type: TransactionType
        
class TransactionCreate(TransactionBase):
    user_id: int
    old_amount: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    # created_at: datetime
        
class TransactionUpdateById(TransactionBase):
    old_amount: Optional[Decimal] = None
    new_amount: Optional[Decimal] = None
    transaction_type: Optional[TransactionType] = None
    user_id: int
    updated_at: datetime

class TransactionUpdateByUserId(TransactionBase):
    updated_at: datetime
    
class TransactionResponse(BaseModel):
    id: int
    user_id: int
    old_amount: Decimal
    new_amount: Decimal
    total_amount: Optional[Decimal]
    transaction_type: TransactionType
    
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    phone_number: str
    # role: UserRole = UserRole.CUSTOMER
    role: str
    wallet_balance: Decimal = 0.0
    transactions: list[TransactionResponse]
    orders: list[schemas.OrderResponse]
    created_at: datetime
    updated_at: datetime
    model_config = {
        "from_attributes": True 
    }