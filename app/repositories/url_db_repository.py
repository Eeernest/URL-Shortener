from app.models.url_model import Url

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

class UrlDbRepository:
  def __init__(self, session: Session):
    self.session = session

  def get_long_url(self, long_url: str) -> Url | None:
    return self.session.execute(select(Url).where(Url.long_url == long_url)).scalar_one_or_none()

  def save(self, url: Url) -> Url:
    try:
      self.session.add(url)
      self.session.commit()
      self.session.refresh(url)

      return url
    
    except IntegrityError as e:
      self.session.rollback()

      raise e