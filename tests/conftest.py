import pytest
from testcontainers.redis import RedisContainer
from testcontainers.postgres import PostgresContainer
import redis

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.url_db import Base

@pytest.fixture(scope="session")
def redis_container():
  with RedisContainer("redis:7") as rdc:
    client = redis.Redis(
      host=rdc.get_container_host_ip(),
      port=rdc.get_exposed_port(6379),
      decode_responses=True
    )

    yield client

@pytest.fixture(scope="session")
def postgres_container():
  with PostgresContainer("postgres:18") as pgc:
    yield pgc

@pytest.fixture(scope="session")
def db_engine(postgres_container):
  engine = create_engine(postgres_container.get_connection_url())

  Base.metadata.create_all(bind=engine)

  yield engine

  engine.dispose()

@pytest.fixture(scope="function")
def db_session(db_engine):
  connection = db_engine.connect()
  transaction = connection.begin()

  SessionLocal = sessionmaker(bind=connection)
  session = SessionLocal()

  try:
    yield session

  finally:
    session.close()
    transaction.rollback()