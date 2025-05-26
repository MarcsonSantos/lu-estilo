from fastapi import FastAPI
from app.db.init_db import init_db
from app.api import users, clients, products, orders, whatsapp_twilio

app = FastAPI()
app.include_router(users.router)
app.include_router(clients.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(whatsapp_twilio.router)

init_db()

@app.on_event("startup")
def on_startup():
    init_db()
