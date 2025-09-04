from app.services.database import get_session, User

def ensure_user(username: str) -> User:
"""Создаёт пользователя при первом обращении и возвращает его."""
with get_session() as s:
user = s.query(User).filter(User.username == username).first()
if not user:
user = User(username=username)
s.add(user)
return user