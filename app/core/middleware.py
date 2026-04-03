import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s = %(message)s")

class LoggingMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next):
    start_time = time.perf_counter()

    logging.info(f"Request: {request.method} {request.url}")

    try:
      response = await call_next(request)

    except Exception as exc:
      process_time = time.perf_counter() - start_time

      logging.error(f"ERROR: {request.method} {request.url} - Process time: {process_time:.4f}s", exc_info=True)

      raise exc

    process_time = time.perf_counter() - start_time

    logging.info(f"Response status: {response.status_code} - Process time: {process_time:.4f}s")

    return response