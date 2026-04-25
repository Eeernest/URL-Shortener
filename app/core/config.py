import os

from dotenv import load_dotenv

load_dotenv(".env")

class Config:
  DATABASE_URL = os.getenv("POSTGRES_URL",  "postgresql://user:pass@localhost/dummy")

  CACHE_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

  TTL = 604800

  CACHE_RL_URL = os.getenv("REDIS_RL_URL", "redis://localhost:6379/0")

  NETLOC = os.getenv("NETLOC")