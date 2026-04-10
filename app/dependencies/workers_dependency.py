from typing import Annotated

from fastapi import Depends

from app.db.url_db import SessionLocal
from app.workers.url_worker import UrlWorker

def get_url_worker():
  session_factory = SessionLocal()

  return UrlWorker(session_factory)

UrlWorkerDep = Annotated[UrlWorker, Depends(get_url_worker)]