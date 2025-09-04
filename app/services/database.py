from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from app.config.settings import DATABASE_URL

# Подключение к PostgreSQL
engine = create_engine(DATABASE_URL, echo=True)  # echo=True чтобы видеть SQL-запросы
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Пример модели
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_seen = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
