from app.db.url_db import SessionDep
from app.repositories.url_db_repository import UrlDbRepository
from app.services.url_service import UrlService

from typing import Annotated
from fastapi import Depends

def get_url_service(session: SessionDep):
  db_repo = UrlDbRepository(session)

  return UrlService(db_repo)

UrlDep = Annotated[UrlService, Depends(get_url_service)]