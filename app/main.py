from fastapi import FastAPI

from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.core.middleware import LoggingMiddleware, limiter
from app.db.url_db import create_db_and_table
from app.routers.url_router import router as url_router

app = FastAPI()

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