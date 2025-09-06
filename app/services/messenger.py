from __future__ import annotations
from telebot import TeleBot
from app.config.settings import TELEGRAM_TOKEN
from app.utils.exceptions import ConfigError

def get_bot() -> TeleBot:
    token = TELEGRAM_TOKEN
    if not token:
        raise ConfigError("TELEGRAM_TOKEN не задан. Установите в .env или переменных окружения.")
    return TeleBot(token, parse_mode="HTML", threaded=True)
