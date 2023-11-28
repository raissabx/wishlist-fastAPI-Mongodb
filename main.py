from fastapi import FastAPI
from routes.route_customer import router as router_customer
from routes.route_product import router as router_product

app = FastAPI(title='Desafio Wishlist')
app.include_router(router_customer)
app.include_router(router_product)



