from sqlalchemy import Column, Integer, String, DateTime, func

from app.db.url_db import Base

class Url(Base):
  __tablename__ = "url"

  id = Column(Integer, primary_key=True)
  long_url = Column(String, nullable=False, index=True)
  short_code = Column(String, unique=True, index=True)
  created = Column(DateTime, nullable=False, default=func.now())
  updated = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
  click_count = Column(Integer, default=0)