import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DB_HOST: str = os.environ.get("DB_HOST")
DB_ROOT: str = os.environ.get("DB_ROOT")
DB_PASSWORD: str = os.environ.get("DB_PASSWORD")
DB_NAME: str = os.environ.get("DB_NAME")

DB_URL: str = f"postgresql+asyncpg://{DB_ROOT}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
TG_TOKEN: str = os.environ.get("TG_TOKEN")
CIPHER_KEY: str = os.environ.get("CIPHER_KEY")
