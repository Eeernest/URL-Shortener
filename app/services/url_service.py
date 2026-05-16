import secrets
import string
from urllib.parse import urlparse

from sqlalchemy.exc import IntegrityError

from app.core.config import Config
from app.core.exceptions import ShortCodeGenerationError, UrlNotFoundError
from app.models.url_model import Url
from app.repositories.url_cache_repository import UrlCacheRepository
from app.repositories.url_db_repository import UrlDbRepository
from app.schemas.url_schema import UrlCreate

class UrlService:
  def __init__(self, db_repo: UrlDbRepository, cache_repo: UrlCacheRepository, config: Config):
    self.db_repo = db_repo
    self.cache_repo = cache_repo
    self.config = config

  def _generate_short_code(self, length=6) -> str:
    characters = string.digits + string.ascii_letters
    return "".join(secrets.choice(characters) for _ in range(length))

  def _extract_short_code(self, short_url: str) -> str:
    path = urlparse(short_url).path
    return path.lstrip("/")
  
  async def _create_url_obj(self, long_url_str: str, retries: int) -> Url:
    for _ in range(retries):
      short_code = self._generate_short_code()
      url_obj = Url(long_url=long_url_str, short_code=short_code)

      try:
        return await self.db_repo.save(url_obj)

      except IntegrityError:
        existing_url_obj = await self.db_repo.get_by_long_url(long_url_str)

        if existing_url_obj is not None:
          return existing_url_obj

        continue

    raise ShortCodeGenerationError(f"Failed to generate a unique code for '{long_url_str}' URL")
  
  async def _resolve_internal_short_url(self, long_url: str) -> Url | None:
    if urlparse(long_url).netloc != self.config.NETLOC:
      return None

    short_code = self._extract_short_code(long_url)
    return await self.db_repo.get_by_short_code(short_code)

  async def get_or_create(self, url: UrlCreate, retries=5) -> Url:
    long_url_str = str(url.long_url)

    resolved_url_obj = await self._resolve_internal_short_url(long_url_str)
    
    if resolved_url_obj is not None:
      return resolved_url_obj

    existing_url_obj = await self.db_repo.get_by_long_url(long_url_str)
    
    if existing_url_obj is not None:
      return existing_url_obj
    
    return await self._create_url_obj(long_url_str, retries)
  
  async def fetch_long_url(self, short_code: str) -> Url:
    url_obj = await self.cache_repo.get_by_short_code(short_code)

    if url_obj is None:
      url_obj = await self.db_repo.get_by_short_code(short_code)

      if url_obj is None:
        raise UrlNotFoundError(f"Short code '{short_code}' not found")
      
      await self.cache_repo.set_url_obj(url_obj)

    return url_obj
  
  async def fetch_stats(self, short_url: str) -> Url:
    short_code = self._extract_short_code(short_url)

    url_obj = await self.db_repo.get_by_short_code(short_code)

    if url_obj is None:
      raise UrlNotFoundError(f"Short URL '{short_url}' not found")
    
    return url_obj