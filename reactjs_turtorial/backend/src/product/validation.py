from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from product import models

def check_product_group_valid (group_id: int, db: Session = Depends(get_db)):
    group = db.query(models.ProductGroup).filter(models.ProductGroup.id == group_id).first()
    if group is None:
        return False
    return True

def check_product_category_valid (category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id).first()
    if category is None:
        return False
    return True