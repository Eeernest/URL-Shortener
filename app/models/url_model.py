from sqlalchemy import Column, Integer, String, DateTime, func

from app.db.url_db import Base

class Url(Base):
  __tablename__ = "url"

  id = Column(Integer, primary_key=True)
  long_url = Column(String, unique=True, nullable=False, index=True)
  short_code = Column(String, unique=True, index=True)
  click_count = Column(Integer, default=0)