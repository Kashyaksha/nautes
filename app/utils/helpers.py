from telebot.types import User as TgUser

def safe_username(tg_user: TgUser) -> str:
    """
    Получаем username; если его нет — формируем по id.
    """
    if tg_user is None:
        return "unknown"
    return tg_user.username or f"id_{tg_user.id}"
