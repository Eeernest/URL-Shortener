from app.db.url_db import SessionLocal
from app.repositories.url_db_repository import UrlDbRepository

def increment_click_task(short_code: str):
  session = SessionLocal()

  try:
    repo = UrlDbRepository(session)
    repo.increment_click(short_code)
  
  finally:
    session.close()