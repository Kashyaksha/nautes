from __future__ import annotations
from typing import Optional, List
from sqlalchemy import create_engine, String, Integer, ForeignKey, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, sessionmaker
from app.config.settings import DATABASE_URL
from app.utils.logger import logger

class Base(DeclarativeBase):
    pass

class City(Base):
    __tablename__ = "cities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    places: Mapped[List["Place"]] = relationship(back_populates="city", cascade="all, delete-orphan")

class Place(Base):
    __tablename__ = "places"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(64), index=True, nullable=False)  # cafe, museum, hospital, etc
    address: Mapped[str] = mapped_column(String(256), nullable=True)
    phone: Mapped[str] = mapped_column(String(64), nullable=True)
    url: Mapped[str] = mapped_column(String(256), nullable=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)

    city: Mapped[City] = relationship(back_populates="places")

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

def init_db(seed: bool = True) -> None:
    """Создаёт таблицы. При seed=True добавляет тестовые данные, если их нет."""
    Base.metadata.create_all(engine)
    if not seed:
        return
    with SessionLocal() as session:
        # Если данных нет — добавим примеры
        existing = session.scalar(select(func.count(Place.id)))
        if existing and existing > 0:
            return
        city = City(name="Алматы")
        session.add(city)
        session.flush()
        places = [
            Place(name="Кафе Central", category="cafe", address="Абая 10", phone="+7 700 000 00 01", url="", city_id=city.id),
            Place(name="Музей Истории", category="museum", address="Достык 5", phone="+7 700 000 00 02", url="", city_id=city.id),
            Place(name="Поликлиника №1", category="hospital", address="Сатпаева 12", phone="+7 700 000 00 03", url="", city_id=city.id),
        ]
        session.add_all(places)
        session.commit()
        logger.info("База инициализирована примерными данными.")

def search_places(session: Session, query: str, limit: int = 5) -> list[Place]:
    q = select(Place).where(Place.name.ilike(f"%{query}%")).limit(limit)
    return list(session.scalars(q))

def search_by_category(session: Session, category: str, limit: int = 10) -> list[Place]:
    q = select(Place).where(Place.category.ilike(f"%{category}%")).limit(limit)
    return list(session.scalars(q))
