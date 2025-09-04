"""
Бизнес-логика: поиск мест, категории, управление избранным и пользователями.
"""
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from app.services.database import get_session, Place, Category, User, Favorite
from app.utils.logger import logger

def get_or_create_user(tg_user):
    """Создаёт пользователя, если его нет, иначе возвращает существующего."""
    with get_session() as db:
        user = db.query(User).filter(User.telegram_id == tg_user.id).first()
        if user:
            return user
        try:
            user = User(
                telegram_id=tg_user.id,
                username=tg_user.username
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            return db.query(User).filter(User.telegram_id == tg_user.id).first()


def list_categories() -> List[Category]:
    with get_session() as s:
        return s.query(Category).order_by(Category.name).all()

def get_places_by_category(category_id: int):
    with get_session() as s:
        return s.query(Place).filter(Place.category_id == category_id).order_by(Place.name).all()

def search_places(query: str):
    """
    Базовый поиск: ищем по имени и описанию (SQL LIKE).
    """
    q = f"%{query}%"
    with get_session() as s:
        return s.query(Place).filter(
            (Place.name.ilike(q)) | (Place.description.ilike(q)) | (Place.address.ilike(q))
        ).order_by(Place.name).all()

def get_place(place_id: int) -> Optional[Place]:
    with get_session() as s:
        return s.query(Place).filter(Place.id == place_id).first()

def add_favorite(user_id: int, place_id: int) -> Favorite:
    with get_session() as s:
        fav = s.query(Favorite).filter(Favorite.user_id == user_id, Favorite.place_id == place_id).first()
        if not fav:
            fav = Favorite(user_id=user_id, place_id=place_id)
            s.add(fav)
            s.flush()
        return fav

def remove_favorite(user_id: int, place_id: int) -> bool:
    with get_session() as s:
        fav = s.query(Favorite).filter(Favorite.user_id == user_id, Favorite.place_id == place_id).first()
        if fav:
            s.delete(fav)
            return True
        return False

def list_user_favorites(user_id: int):
    with get_session() as s:
        return s.query(Favorite).filter(Favorite.user_id == user_id).all()
