import os

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.exceptions import AppBaseException
from app.core.exception_handlers import custom_exc_handler, validation_exc_handler, rate_limit_exc_handler, general_exc_handler
from app.core.middleware import LoggingMiddleware, limiter
from app.db.url_db import create_db_and_table
from app.routers.url_router import router as url_router

app = FastAPI()

origins = [
  os.getenv("FRONT_URL")
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["POST", "GET", "OPTIONS"],
  allow_headers=["Content-Type"]
)

app.add_exception_handler(AppBaseException, custom_exc_handler)
app.add_exception_handler(RequestValidationError, validation_exc_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exc_handler)
app.add_exception_handler(Exception, general_exc_handler)

app.add_middleware(SlowAPIMiddleware)

app.add_middleware(LoggingMiddleware)

app.state.limiter = limiter

@app.on_event("startup")
def on_startup():
  create_db_and_table()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def read_index():
  return FileResponse("app/templates/index.html")

app.include_router(url_router)