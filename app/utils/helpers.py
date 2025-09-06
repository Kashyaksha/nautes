from __future__ import annotations
from telebot.types import User as TgUser

def safe_username(tg_user: TgUser) -> str:
    username = getattr(tg_user, "username", None)
    if username:
        return f"@{username}"
    # Склеим имя из доступных полей
    first = getattr(tg_user, "first_name", "") or ""
    last = getattr(tg_user, "last_name", "") or ""
    full = (first + " " + last).strip()
    return full or f"id:{tg_user.id}"
