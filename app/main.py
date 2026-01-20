from fastapi import FastAPI
from app.api.orders.router import router as orders_router

app = FastAPI(title="Aiti Guru Test")
app.include_router(orders_router)
