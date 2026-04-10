import logging
import time

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import Config

limiter = Limiter(key_func=get_remote_address, storage_uri=Config.REDIS_RL_URL)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s = %(message)s")

class LoggingMiddleware(BaseHTTPMiddleware):
  def dispatch(self, request: Request, call_next):
    start_time = time.perf_counter()

    logging.info(f"Request: {request.method} {request.url}")

    response = call_next(request)

    process_time = time.perf_counter() - start_time

    logging.info(f"Response status: {response.status_code} - Process time: {process_time:.4f}s")

    return response