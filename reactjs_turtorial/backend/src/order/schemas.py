from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

# Order schema 
class OrderBase(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    
class OrderCreate(OrderBase):
    id: Optional[int]= None
    user_id: int
    total_amount: Decimal
    # order_date: datetime
    
class OrderUpdate(OrderBase):
    user_id: Optional[int]
    total_amount: Optional[Decimal]
    updated_at: datetime
    
class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    order_date: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }
    
# Order detail schema 
class OrderDetail(BaseModel):
    product_id: int
    product_name: str
    product_image: str
    quantity: int
    unit_price: Decimal
    
class OrderDetailCreate(OrderDetail):
    order_id: int
    # created_at: datetime
    
class OrderDetailUpdate(OrderDetail):
    updated_at: datetime
    
class OrderDetailResponse(BaseModel):
    id: int
    order_id: int
    order: OrderResponse
    product_name: str
    product_image: str
    product_id: int
    quantity: int
    unit_price: Decimal
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }
    
