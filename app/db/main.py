from fastapi import FastAPI

from app.db.url_db import create_db_and_table

app = FastAPI()

@app.on_event("startup")
def on_startup():
  create_db_and_table()

@app.get("/")
def read_root():
  return {"message": "hello"}