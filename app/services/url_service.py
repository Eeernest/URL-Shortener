from app.core.exceptions import ShortCodeGenerationError, UrlNotFoundError
from app.models.url_model import Url
from app.schemas.url_schema import UrlCreate
from app.repositories.url_db_repository import UrlDbRepository
from app.repositories.url_cache_repository import UrlCacheRepository

from sqlalchemy.exc import IntegrityError

import string
import secrets

class UrlService:
  def __init__(self, db_repo: UrlDbRepository, cache_repo: UrlCacheRepository):
    self.db_repo = db_repo
    self.cache_repo = cache_repo

  def _generate_short_code(self, length=6) -> str:
    characters = string.digits + string.ascii_letters
    return "".join(secrets.choice(characters) for _ in range(length))


      
  def get_or_create(self, url: UrlCreate, retries=5) -> Url:
    existing_url_obj = self.db_repo.get_by_long_url(str(url.long_url))

    if existing_url_obj is not None:
      return existing_url_obj
    
    for _ in range(retries):
      short_code = self._generate_short_code()
      url_obj = Url(long_url=str(url.long_url), short_code=short_code)

      try:
        return self.db_repo.save(url_obj)

      except IntegrityError:
        continue

    raise ShortCodeGenerationError(f"Failed to generate a unique code for '{url.long_url}' URL")
  
  def fetch_long_url(self, short_code: str) -> Url:
    url_obj = self.cache_repo.get_by_short_code(short_code)

    if url_obj is None:
      url_obj = self.db_repo.get_by_short_code(short_code)

      if url_obj is None:
        raise UrlNotFoundError(f"Short code '{short_code}' not found")
      
      self.cache_repo.set_url_obj(url_obj)

    return url_obj