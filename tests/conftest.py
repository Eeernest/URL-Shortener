import pytest
import redis
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from app.db.url_db import Base
from app.core.middleware import limiter

@pytest.fixture(scope="session")
def anyio_backend():
  return "asyncio"

@pytest.fixture(scope="session")
def redis_container():
  with RedisContainer("redis:7") as rdc:
    client = redis.Redis(
      host=rdc.get_container_host_ip(),
      port=rdc.get_exposed_port(6379),
      decode_responses=True
    )

    yield client

@pytest.fixture(autouse=True)
def clear_redis_container(redis_container):
  redis_container.flushall()

@pytest.fixture(scope="session", autouse=True)
def disable_limiter(redis_container):
  limiter.enabled = False

@pytest.fixture(scope="session")
def postgres_container():
  with PostgresContainer("postgres:16-alpine") as postgres:
    yield postgres

@pytest.fixture(scope="session")
def test_engine(postgres_container):
  url = postgres_container.get_connection_url().replace("postgresql+psycopg2", "postgresql+asyncpg")

  engine = create_async_engine(
    url,
    poolclass=NullPool,
  )

  return engine

@pytest.fixture(scope="session")
async def setup_database(test_engine):
  async with test_engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  yield 

  async with test_engine.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all)
  
  await test_engine.dispose()

@pytest.fixture
async def db_session(test_engine, setup_database):
  conn = await test_engine.connect()
  trans = await conn.begin()

  test_async_session = async_sessionmaker(
    bind=conn,
    class_=AsyncSession,
    expire_on_commit=False,
    join_transaction_mode="create_savepoint"
  )

  async with test_async_session() as session:
    try:
      yield session
    finally:
      await session.close()
      await trans.rollback()
      await conn.close()