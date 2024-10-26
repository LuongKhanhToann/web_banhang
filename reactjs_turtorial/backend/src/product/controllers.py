from sqlalchemy import func
from database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from product import models
from product import schemas
from product import validation
from unidecode import unidecode
from typing import List


# Product controller 
def get_products(limit: int = 5, offset: int = 0, db: Session = Depends(get_db)) -> dict:
    db_products = db.query(models.Product).offset(offset).limit(limit).all()
    total_products = db.query(models.Product).count()
    if not db_products:
        raise HTTPException(status_code=404, detail="No products found")
    return {
        "products": [schemas.ProductResponse.model_validate(products) for products in db_products],
        "total": total_products,
    }
    
def get_all_products(db: Session = Depends(get_db)) -> List[schemas.ProductResponse]:
    db_products = db.query(models.Product).all()
    if not db_products:
        raise HTTPException(status_code=404, detail="No products found")
    return db_products

def get_product_by_id(product_id: int, db: Session = Depends(get_db)) -> schemas.ProductResponse:
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.ProductResponse.model_validate(product)

def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)) -> schemas.ProductResponse:
    if not validation.check_product_group_valid(product.group_id, db):
        raise HTTPException(status_code=404, detail="Product group not found")
    if not validation.check_product_category_valid(product.category_id, db):
        raise HTTPException(status_code=404, detail="Product category not found")
    
    # db_product = models.Product(name=product.name, image=product.image, price=product.price, discount_price=product.discount_price, quantity=product.quantity, description=product.description, supplier=product.supplier, group_id=product.group_id, category_id=product.category_id, created_at=product.created_at, updated_at=product.updated_at)
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return schemas.ProductResponse.model_validate(db_product)

def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)) -> schemas.ProductResponse:
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product.model_dump(exclude_unset=True)
    
    db.query(models.Product).filter(models.Product.id == product_id).update(update_data)
    
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

# product group controller 
def get_product_groups(limit: int = 5, offset: int = 0, db: Session = Depends(get_db)) -> dict:
    db_groups = db.query(models.ProductGroup).offset(offset).limit(limit).all()
    total_groups = db.query(models.ProductGroup).count()
    if not db_groups:
        raise HTTPException(status_code=404, detail="No product groups found")
    return {
        "groups": [schemas.ProductGroupResponse.model_validate(group) for group in db_groups],
        "total": total_groups,
    }

def get_product_group_by_id(group_id: int, db: Session = Depends(get_db)) -> schemas.ProductGroupResponse:
    group = db.query(models.ProductGroup).filter(models.ProductGroup.id == group_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Product group not found")
    return schemas.ProductGroupResponse.model_validate(group)

def create_product_group(group: schemas.ProductGroupCreate, db: Session = Depends(get_db)) -> schemas.ProductGroupResponse:
    db_group = models.ProductGroup(**group.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def update_product_group(group_id: int, group: schemas.ProductGroupUpdate, db: Session = Depends(get_db)) -> schemas.ProductGroupResponse:
    db_group = db.query(models.ProductGroup).filter(models.ProductGroup.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Product group not found")
    
    update_data = group.model_dump(exclude_unset=True)
    # update_data['updated_at'] = datetime.utcnow()
    db.query(models.ProductGroup).filter(models.ProductGroup.id == group_id).update(update_data)
    
    db.commit()
    db.refresh(db_group)
    
    return schemas.ProductGroupResponse.model_validate(db_group)

def delete_product_group(group_id: int, db: Session = Depends(get_db)):
    db_group = db.query(models.ProductGroup).filter(models.ProductGroup.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Product group not found")
    db.delete(db_group)
    db.commit()
    return {"message": "Product group deleted successfully"}

# product category controller 

def get_product_categories(limit: int = 5, offset: int = 0, db: Session = Depends(get_db)) -> dict:
    db_categories = db.query(models.ProductCategory).offset(offset).limit(limit).all()
    total_categories = db.query(models.ProductCategory).count()
    if not db_categories:
        raise HTTPException(status_code=404, detail="No product categories found")
    return {
        "categories": [schemas.ProductCategoryResponse.model_validate(category) for category in db_categories],
        "total": total_categories,
    }

def get_product_category_by_id(category_id: int, db: Session = Depends(get_db)) -> schemas.ProductCategoryResponse:
    category = db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Product category not found")
    return schemas.ProductCategoryResponse.model_validate(category)

def create_product_category(category: schemas.ProductCategoryCreate, db: Session = Depends(get_db)) -> schemas.ProductCategoryResponse:
    if not validation.check_product_group_valid(category.group_id, db):
        raise HTTPException(status_code=404, detail="Product group not found")
    
    db_category = models.ProductCategory(**category.model_dump())    

    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return schemas.ProductCategoryResponse.model_validate(db_category)

def update_product_category(category_id: int, category: schemas.ProductCategoryUpdate, db: Session = Depends(get_db)) -> schemas.ProductCategoryResponse:    
    db_category = db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Product category not found")
    
    update_data = category.model_dump(exclude_unset=True)
    db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id).update(update_data)
    
    db.commit()
    db.refresh(db_category)
    return schemas.ProductCategoryResponse.model_validate(db_category)

def delete_product_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Product category not found")
    db.delete(db_category)
    db.commit()
    return {"message": "Product category deleted successfully"}

# search controller 
def search_products(form: schemas.ProductSearch, db: Session = Depends(get_db)) -> schemas.ProductResponse:
    query = db.query(models.Product).join(models.ProductCategory).join(models.ProductGroup)
    if form.group_name:
        form.group_name = form.group_name.strip()
        query = query.filter(func.lower(func.unaccent(models.ProductGroup.name)).like(f"%{unidecode(form.group_name.lower())}%"))
    if form.category_name:
        form.category_name = form.category_name.strip()
        query = query.filter(func.lower(func.unaccent(models.ProductCategory.name)).like(f"%{unidecode(form.category_name.lower())}%"))
    if form.product_name:
        form.product_name = form.product_name.strip()
        query = query.filter(func.lower(func.unaccent(models.Product.name)).like(f"%{unidecode(form.product_name.lower())}%"))
    if form.supplier:
        form.supplier = form.supplier.strip()
        query = query.filter(func.lower(func.unaccent(models.Product.supplier)).like(f"%{unidecode(form.supplier.lower())}%"))
    if form.min_price and not form.max_price:
        query = query.filter(models.Product.price >= form.min_price)
    if form.max_price and not form.min_price:
        query = query.filter(models.Product.price <= form.max_price)
    if form.min_price and form.max_price:
        query = query.filter(models.Product.price >= form.min_price).filter(models.Product.price <= form.max_price)
    if form.discount_price is True:
        query = query.filter(models.Product.discount_price > 0)
    if form.quantity is True:
        query = query.filter(models.Product.quantity > 0)
    
    db_products = query.all()
    
    if not db_products:
        raise HTTPException(status_code=404, detail="Products not found")
    
    return [schemas.ProductResponse.model_validate(product) for product in db_products]