from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from order import models
from database import get_db
from order import validation
from typing import List

from order import schemas

def get_orders(db: Session = Depends(get_db)) -> List[schemas.OrderResponse]:
    db_orders = db.query(models.Order).all()
    if not db_orders:
        raise HTTPException(status_code=404, detail="Orders not found")

    return [schemas.OrderResponse.model_validate(order) for order in db_orders]

def get_order_by_id(order_id: int, db: Session = Depends(get_db)) -> schemas.OrderResponse:
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return schemas.OrderResponse.model_validate(order)

def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)) -> schemas.OrderResponse:
    if not validation.check_user_id_valid(order.user_id, db):
        raise HTTPException(status_code=404, detail="User not found")
    
    # db_order = models.Order(user_id=order.user_id, total_amount=order.total_amount, order_date = order.order_date)
    db_order = models.Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return schemas.OrderResponse.model_validate(db_order)

def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)) -> schemas.OrderResponse:
    if not validation.check_user_id_valid(order.user_id, db):
        raise HTTPException(status_code=404, detail="User not found")
    
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    update_data = order.model_dump(exclude_unset=True)
    db.query(models.Order).filter(models.Order.id == order_id).update(update_data)
    
    db.commit()
    db.refresh(db_order)
    return schemas.OrderResponse.model_validate(db_order)

def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return db_order

def get_order_by_id(order_id: int, db: Session = Depends(get_db)) -> schemas.OrderResponse:
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return schemas.OrderResponse.model_validate(order)

def get_orders_by_user_id(user_id: int, db: Session = Depends(get_db)) -> List[schemas.OrderResponse]:
    orders = db.query(models.Order).filter(models.Order.user_id == user_id).all()
    if orders is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return [schemas.OrderResponse.model_validate(order) for order in orders]

def get_orders_by_date(order_date: str, db: Session = Depends(get_db)) -> List[schemas.OrderResponse]:
    orders = db.query(models.Order).filter(models.Order.order_date >= order_date, models.Order.order_date <= order_date).all()
    if orders is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return [schemas.OrderResponse.model_validate(order) for order in orders]

def get_orders_by_date_range(from_date: str, to_date: str, db: Session = Depends(get_db)) -> List[schemas.OrderResponse]:
    orders = db.query(models.Order).filter(models.Order.order_date >= from_date, models.Order.order_date <= to_date).all()
    if orders is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return [schemas.OrderResponse.model_validate(order) for order in orders]

# order detail 
def get_all_order_details(db: Session = Depends(get_db)) -> List[schemas.OrderDetailResponse]:
    db_details = db.query(models.OrderDetail).all()
    if not db_details:
        raise HTTPException(status_code=404, detail="Order Details not found")
    return [schemas.OrderDetailResponse.model_validate(detail) for detail in db_details]

def get_order_details(order_id: int, db: Session = Depends(get_db)) -> List[schemas.OrderDetailResponse]:
    order_details = db.query(models.OrderDetail).filter(models.OrderDetail.order_id == order_id).all()
    if order_details is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return [schemas.OrderDetailResponse.model_validate(detail) for detail in order_details]

def create_order_detail(order_detail: schemas.OrderDetailCreate, db: Session = Depends(get_db)) -> schemas.OrderDetailResponse:
    if not validation.check_order_id_valid(order_detail.order_id, db):
        raise HTTPException(status_code=404, detail="Order not found")
    
    # db_order_detail = models.OrderDetail(order_id=order_detail.order_id, product_id=order_detail.product_id, quantity=order_detail.quantity, unit_price=order_detail.unit_price, created_at=order_detail.created_at)
    db_order_detail = models.OrderDetail(**order_detail.model_dump())
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return schemas.OrderDetailResponse.model_validate(db_order_detail)

def update_order_detail(order_detail_id: int, order_detail: schemas.OrderDetailUpdate, db: Session = Depends(get_db)) -> schemas.OrderDetailResponse:
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="Order Detail not found")
    # db_order_detail.product_id = order_detail.product_id
    # db_order_detail.quantity = order_detail.quantity
    # db_order_detail.unit_price = order_detail.unit_price
    # db_order_detail.updated_at = order_detail.updated_at
    update_data = order_detail.model_dump(exclude_unset=True)
    
    db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).update(update_data)
    
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

def delete_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="Order Detail not found")
    db.delete(db_order_detail)
    db.commit()
    return db_order_detail