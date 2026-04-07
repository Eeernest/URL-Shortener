from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.middleware import LoggingMiddleware, limiter
from app.db.url_db import create_db_and_table
from app.routers.url_router import router as url_router

app = FastAPI()

origins = [
  "http://127.0.0.1:5500"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["POST", "GET"],
  allow_headers=["Content-Type"]
)

app.add_middleware(SlowAPIMiddleware)

app.add_middleware(LoggingMiddleware)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.on_event("startup")
def on_startup():
  create_db_and_table()

@app.get("/")
def read_root():
  return {"message": "hello"}

app.include_router(url_router)