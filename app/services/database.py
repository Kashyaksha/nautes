import datetime
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from app.config.settings import DATABASE_URL


# Настройка движка
engine = create_engine(
    DATABASE_URL,
    echo=False,  # поставь True для отладки SQL
    pool_pre_ping=True,
    future=True,
)

# Фабрика сессий и scoped_session для потокобезопасности
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
SessionLocal = scoped_session(SessionFactory)

# База моделей
Base = declarative_base()


# Модели
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, index=True, nullable=True)
    first_seen = Column(DateTime, default=datetime.datetime.utcnow)


def init_db() -> None:
    """Создаёт таблицы, если их ещё нет"""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_session():
    """Контекстный менеджер для безопасной работы с сессией"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        logging.exception(f"Database error: {e}")
        session.rollback()
        raise
    finally:
        session.close()
