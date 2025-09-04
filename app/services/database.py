# app/services/database.py
import datetime
from contextlib import contextmanager
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Float,
    ForeignKey,
    BigInteger,
    inspect,
    text,
)
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session, relationship
from app.config.settings import DATABASE_URL
from app.utils.logger import logger

# Engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    future=True,
)

# Session factory
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
SessionLocal = scoped_session(SessionFactory)

Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)  # ✅ уникальный идентификатор
    username = Column(String(255), nullable=True, index=True)  # ❌ убрали unique
    first_seen = Column(DateTime, default=datetime.datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    places = relationship("Place", back_populates="category")


class Place(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    address = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    category = relationship("Category", back_populates="places")
    favorites = relationship("Favorite", back_populates="place", cascade="all, delete-orphan")


class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    added_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="favorites")
    place = relationship("Place", back_populates="favorites")


def ensure_telegram_column():
    """
    Если таблица users существует, но в ней нет столбца telegram_id,
    добавляем его (как nullable). Создаём индекс (если возможно).
    """
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if "users" in tables:
            cols = [c["name"] for c in inspector.get_columns("users")]
            if "telegram_id" not in cols:
                logger.info("Добавляем колонку 'telegram_id' в таблицу users...")
                with engine.begin() as conn:
                    # добавляем колонку как BIGINT (telegram id может быть большим)
                    conn.execute(text("ALTER TABLE users ADD COLUMN telegram_id BIGINT"))
                    # создаём индекс для ускорения поиска (IF NOT EXISTS поддерживается в PG)
                    try:
                        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_users_telegram_id ON users (telegram_id)"))
                    except Exception as e:
                        # для SQLite или старых версий PG может не сработать — просто логируем
                        logger.warning("Не получилось создать индекс ix_users_telegram_id: %s", e)
                logger.info("Колонка 'telegram_id' добавлена.")
    except Exception as e:
        logger.exception("Ошибка при попытке проверить/создать колонку telegram_id: %s", e)
        # не прерываем инициализацию — дальше create_all() уже выполнен или будет обработан


def init_db() -> None:
    """
    Создаёт отсутствующие таблицы и гарантирует, что колонка telegram_id существует.
    """
    logger.info("Creating DB tables (if not exists)...")
    Base.metadata.create_all(bind=engine)
    # если таблицы уже были — create_all ничего не изменит; поэтому явно проверим колонку
    ensure_telegram_column()

@contextmanager
def get_session():
    """
    Контекстный менеджер для сессий SQLAlchemy.
    Использование:
        with get_session() as s:
            s.add(...)
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.exception("Database session error: %s", e)
        session.rollback()
        raise
    finally:
        session.close()
