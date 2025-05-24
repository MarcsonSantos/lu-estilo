from fastapi import FastAPI
from app.db.init_db import init_db
from app.api import users, clients

app = FastAPI()
app.include_router(users.router)
app.include_router(clients.router)

@app.on_event("startup")
def on_startup():
    init_db()
