from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.url_model import Url

class UrlDbRepository:
  def __init__(self, session: AsyncSession):
    self.session = session
  
  async def get_by_long_url(self, long_url: str) -> Url | None:
    result = await self.session.execute(select(Url).where(Url.long_url == long_url))

    return result.scalar_one_or_none()

  async def get_by_short_code(self, short_code: str) -> Url | None:
    result = await self.session.execute(select(Url).where(Url.short_code == short_code))

    return result.scalar_one_or_none()

  async def save(self, url: Url) -> Url:
    try:
      self.session.add(url)
      await self.session.commit()
      await self.session.refresh(url)

      return url
    except IntegrityError as exc:
      await self.session.rollback()

      raise exc

  async def increment_click(self, short_code: str):
    await self.session.execute(update(Url).where(Url.short_code == short_code).values(click_count=Url.click_count + 1).execution_options(synchronize_session=False))
    await self.session.commit()