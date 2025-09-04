from telebot.types import User as TgUser

def safe_username(tg_user: TgUser) -> str:
    return tg_user.username or f"id_{tg_user.id}"