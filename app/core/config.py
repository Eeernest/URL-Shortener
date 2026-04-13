import os

from dotenv import load_dotenv

load_dotenv(".env")

class Config:
  DATABASE_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT', 5432)}/{os.getenv('POSTGRES_DB')}"

  REDIS_URL = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}/0"

  TTL = 604800

  REDIS_RL_URL = f"redis://{os.getenv('REDIS_RL_HOST', 'localhost')}:{os.getenv('REDIS_RL_PORT', 6379)}/0"

  NETLOC = os.getenv("NETLOC")