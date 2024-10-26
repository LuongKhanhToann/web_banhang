from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Product schema
class ProductBase(BaseModel):
    name: str
    image: str    
    price: float
    discount_price: float
    quantity: int
    description: str
    supplier: str
    
        
class ProductCreate(ProductBase):
    group_id: int
    category_id: int
    # created_at: datetime
    # updated_at: datetime
    
    model_config = {
        "from_attributes": True 
    }
        
class ProductUpdate(ProductBase):
    name: Optional[str] = None
    image: Optional[str] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
    supplier: Optional[str] = None
    updated_at: datetime
    
    
        
# Product group schema
class ProductGroup(BaseModel):
    name: str
    
        
class ProductGroupCreate(ProductGroup):
    # created_at: datetime
    pass
    
        
class ProductGroupUpdate(BaseModel):
    name: Optional[str]
    # updated_at: datetime
    
class ProductGroupResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }
    

# Product category schema
class ProductCategory(BaseModel):
    name: str
    
        
class ProductCategoryCreate(ProductCategory):
    group_id: int
    # created_at: datetime
    
    
class ProductCategoryUpdate(ProductCategory):
    name: Optional[str] 
    group_id: Optional[int] 
    # updated_at: datetime
    
class ProductCategoryResponse(BaseModel):
    id: int
    name: str
    group_id: int
    product_group: ProductGroupResponse
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }
    

class ProductSearch(BaseModel):
    group_name: Optional[str] = None
    category_name: Optional[str] = None
    product_name: Optional[str] = None
    supplier: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    discount_price: Optional[bool] = None
    quantity: Optional[bool] = None
    
class ProductResponse(BaseModel):
    id: int
    name: str
    image: str    
    price: float
    discount_price: float
    quantity: int
    description: str
    supplier: str
    group_id: int
    category_id: int
    product_category: ProductCategoryResponse
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }