from fastapi import FastAPI
from src.database import Base, engine
from src.routers import products

# Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API каталога товаров готов к работе"}

app.include_router(products.router)