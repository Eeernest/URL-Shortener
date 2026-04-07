from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.url_model import Url

class UrlDbRepository:
  def __init__(self, session: Session):
    self.session = session

  def get_by_long_url(self, long_url: str) -> Url | None:
    return self.session.execute(select(Url).where(Url.long_url == long_url)).scalar_one_or_none()
  
  def get_by_short_code(self, short_code: str) -> Url | None:
    return self.session.execute(select(Url).where(Url.short_code == short_code)).scalar_one_or_none()

  def save(self, url: Url) -> Url:
    try:
      self.session.add(url)
      self.session.commit()
      self.session.refresh(url)

      return url
    
    except IntegrityError as exc:
      self.session.rollback()

      raise exc
    
  def increment_click(self, short_code: str):
    self.session.execute(update(Url).where(Url.short_code == short_code).values(click_count=Url.click_count + 1).execution_options(synchronize_session=False))
    self.session.commit()