import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.url_db import Base

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db_session():
  Base.metadata.create_all(bind=engine)
  session = TestSessionLocal()

  try:
    yield session

  finally:
    session.close()
    Base.metadata.drop_all(bind=engine)