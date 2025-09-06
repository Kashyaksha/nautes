"""Загрузка конфигурации из .env с безопасными значениями по умолчанию."""
from __future__ import annotations
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN: str | None = os.getenv("TELEGRAM_TOKEN")

# БД: если явно не указана PostgreSQL — используем SQLite по умолчанию (локальная разработка)
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")

if all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB]):
    DATABASE_URL = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
else:
    BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DATADIR = os.path.join(BASEDIR, "data")
    os.makedirs(DATADIR, exist_ok=True)
    db_path = os.path.join(DATADIR, "database.sqlite")
    DATABASE_URL = f"sqlite:///{db_path}"
