from sqlalchemy.orm import sessionmaker

from app.repositories.url_db_repository import UrlDbRepository

class UrlWorker:
  def __init__(self, sessionmaker: sessionmaker):
    self.session_factory = sessionmaker

  def increment_click(self, short_code: str):
    with self.session_factory() as session:
      repo = UrlDbRepository(session)

      repo.increment_click(short_code)