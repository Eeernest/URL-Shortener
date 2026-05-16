from sqlalchemy.ext.asyncio import async_sessionmaker

from app.repositories.url_db_repository import UrlDbRepository

class UrlWorker:
  def __init__(self, sessionmaker: async_sessionmaker):
    self.session_factory = sessionmaker

  async def increment_click(self, short_code: str):
    async with self.session_factory() as session:
      repo = UrlDbRepository(session)

      await repo.increment_click(short_code)