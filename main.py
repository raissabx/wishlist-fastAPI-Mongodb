from fastapi import FastAPI
from routes.route_customer import router as router_customer
from routes.route_product import router as router_product
from routes.route_product_api import router as router_product_api
from routes.route_auth import router as router_auth


app = FastAPI(title='Desafio Wishlist')


app.include_router(router_customer)
app.include_router(router_product)
app.include_router(router_product_api)
app.include_router(router_auth)
