import os

from dotenv import load_dotenv

load_dotenv(".env")

class Config:
  DATABASE_URL = os.getenv("POSTGRES_URL")

  CACHE_URL = os.getenv("REDIS_URL")

  TTL = 604800

  CACHE_RL_URL = os.getenv("REDIS_RL_URL")

  NETLOC = os.getenv("NETLOC")