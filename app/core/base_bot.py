import telebot
from app.config.settings import TELEGRAM_TOKEN
from app.utils.exceptions import ConfigError


if not TELEGRAM_TOKEN:
    raise ConfigError("TELEGRAM_TOKEN отсутствует. Добавь его в .env")


# parse_mode можно поменять при необходимости
bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode="HTML")