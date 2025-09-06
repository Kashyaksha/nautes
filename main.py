"""
Точка входа: создаёт БД и запускает Telegram-бота.
"""
from app.services.database import init_db
from app.telegram.telegram_bot import run
from app.utils.logger import logger

if __name__ == "__main__":
    logger.info("Инициализация базы данных...")
    init_db(seed=True)
    logger.info("Запуск Telegram-бота...")
    run()
