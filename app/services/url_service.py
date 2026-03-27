from app.models.url_model import Url
from app.schemas.url_schema import UrlCreate
from app.repositories.url_db_repository import UrlDbRepository

import string
import secrets

class UrlService:
  def __init__(self, db_repo: UrlDbRepository):
    self.db_repo = db_repo

  def _generate_short_code(self, length=6) -> str:
    characters = string.digits + string.ascii_letters

    while True:
      new_code = "".join(secrets.choice(characters) for char in range(length))

      if self.db_repo.get_short_code(new_code) is None:
        return new_code
      
  def create_short_code(self, url: UrlCreate) -> Url:
    short_code = Url(
      long_url=str(url.long_url),
      short_code= str(self._generate_short_code())
    )

    return self.db_repo.save(short_code)
  
  def create_short_url(self, base_url: str, short_code: str) -> str:
    return f"{base_url.rstrip('/')}/{short_code}"