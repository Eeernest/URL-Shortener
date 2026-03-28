from app.models.url_model import Url
from app.schemas.url_schema import UrlCreate
from app.repositories.url_db_repository import UrlDbRepository

from sqlalchemy.exc import IntegrityError

import string
import secrets

class UrlService:
  def __init__(self, db_repo: UrlDbRepository):
    self.db_repo = db_repo

  def _generate_short_code(self, length=6) -> str:
    characters = string.digits + string.ascii_letters
    return "".join(secrets.choice(characters) for _ in range(length))
      
  def get_or_create(self, url: UrlCreate, retries=5) -> Url:
    existing_long_url = self.db_repo.get_long_url(str(url.long_url))

    if existing_long_url is not None:
      return existing_long_url
    
    for _ in range(retries):
      short_code = self._generate_short_code()
      url_obj = Url(long_url=url.long_url, short_code=short_code)

      try:
        return self.db_repo.save(url_obj)
      
      except IntegrityError:
        continue

    raise RuntimeError("Failed to generate a unique short_code after several attempts")

  def create_short_url(self, base_url: str, short_code: str) -> str:
    return f"{base_url.rstrip('/')}/{short_code}"