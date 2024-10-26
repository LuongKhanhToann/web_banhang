from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

# from auth import routes
from user import routes as user_routes
from product import routes as product_routes
from order import routes as order_routes

from user.models import User, Transaction
from order.models import Order
from product.models import Product, ProductGroup, ProductCategory

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router, prefix="/api")
app.include_router(user_routes.transaction_router, prefix="/api")

app.include_router(product_routes.product_router, prefix="/api")
app.include_router(product_routes.product_group_router, prefix="/api")
app.include_router(product_routes.product_category_router, prefix="/api")
app.include_router(product_routes.search_product_router, prefix="/api")

app.include_router(order_routes.order_router, prefix="/api")
app.include_router(order_routes.order_detail_router, prefix="/api")


