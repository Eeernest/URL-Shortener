from fastapi import FastAPI

from app.db.url_db import create_db_and_table
from app.routers.url_router import router as url_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
  create_db_and_table()

@app.get("/")
def read_root():
  return {"message": "hello"}

app.include_router(url_router)