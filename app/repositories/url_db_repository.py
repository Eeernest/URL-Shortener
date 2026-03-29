from app.models.url_model import Url

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

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
    
    except IntegrityError as e:
      self.session.rollback()

      raise e
    
  def increase_click_count(self, short_code: str, count: int):
    url_obj = self.get_by_short_code(short_code)

    url_obj.click_count += 1
    self.save(url_obj)