from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded

from app.core.exceptions import AppBaseException

def custom_exc_handler(request: Request, exc: AppBaseException):
  return JSONResponse(
    status_code=exc.status_code,
    content={"detail": exc.detail}
  )

def validation_exc_handler(request: Request, exc: RequestValidationError):
  return JSONResponse(
    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    content={
      "detail": "Wrong input data",
      "errors": exc.errors()
    }
  )

def rate_limit_exc_handler(request: Request, exc: RateLimitExceeded):
  return JSONResponse(
    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    content={"detail": "Too many requests. Try later"}
  )

def general_exc_handler(request: Request, exc: Exception):
  return JSONResponse(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    content={"detail": "Something went wrong. Please try again later."}
  )