from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from order import models
from order import schemas

from order import controllers
from typing import List

order_router = APIRouter(prefix="/order", tags=['Order'])
order_detail_router = APIRouter(prefix="/order_detail", tags=['Order Detail'])

@order_router.get("", response_model=List[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@order_router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    return controllers.get_order_by_id(order_id, db)

@order_router.get("/user/{user_id}", response_model=List[schemas.OrderResponse])
def get_orders_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return controllers.get_orders_by_user_id(user_id, db)

@order_router.post("", status_code=201, response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return controllers.create_order(order, db)

@order_router.put("/{order_id}", response_model=schemas.OrderResponse)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    return controllers.update_order(order_id, order, db)

@order_router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return controllers.delete_order(order_id, db)

@order_router.get("/date", response_model=List[schemas.OrderResponse])
def get_orders_by_date(order_date: str, db: Session = Depends(get_db)):
    return controllers.get_orders_by_date(order_date, db)

@order_router.get("/date_range", response_model=List[schemas.OrderResponse])
def get_orders_by_date_range(start_date: str, end_date: str, db: Session = Depends(get_db)):
    return controllers.get_orders_by_date_range(start_date, end_date, db)


# order detail 
@order_detail_router.get("", response_model=List[schemas.OrderDetailResponse])
def get_all_order_details(db: Session = Depends(get_db)):
    return controllers.get_all_order_details(db)

@order_detail_router.get("/{order_id}", response_model=List[schemas.OrderDetailResponse])
def get_order_detail(order_id: int, db: Session = Depends(get_db)):
    return controllers.get_order_details(order_id, db)

@order_detail_router.post("", status_code=201, response_model=schemas.OrderDetailResponse)
def create_order_detail(order_detail: schemas.OrderDetailCreate, db: Session = Depends(get_db)):
    return controllers.create_order_detail(order_detail, db)

@order_detail_router.put("/{order_detail_id}", response_model=schemas.OrderDetailResponse)
def update_order_detail(order_detail: schemas.OrderDetailUpdate, db: Session = Depends(get_db)):
    return controllers.update_order_detail(order_detail, db)

@order_detail_router.delete("/{order_detail_id}")
def delete_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    return controllers.delete_order_detail(order_detail_id, db)