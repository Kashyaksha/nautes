"""
Инициализация TeleBot.
"""
from telebot import TeleBot, logger as tb_logger
from app.config.settings import TELEGRAM_TOKEN
from app.utils.exceptions import ConfigError
from app.utils.logger import logger

if not TELEGRAM_TOKEN:
    raise ConfigError("TELEGRAM_TOKEN is not set. Add it to .env")

# Включим логирование TeleBot на уровень INFO
tb_logger.setLevel("INFO")

# Создаём bot
bot = TeleBot(TELEGRAM_TOKEN, parse_mode="HTML")
logger.info("TeleBot initialized")
