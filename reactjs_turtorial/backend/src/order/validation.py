from sqlalchemy.orm import Session
from user import models
from order import models as order_models

def check_user_id_valid(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        return False
    return True

def check_order_id_valid(order_id: int, db: Session):
    order = db.query(order_models.Order).filter(order_models.Order.id == order_id).first()
    if order is None:
        return False
    return True

def check_order_detail_id_valid(order_detail_id, db: Session):
    order_detail = db.query(order_models.OrderDetail).filter(order_models.OrderDetail.id == order_detail_id).first()
    if order_detail is None:
        return False
    return True