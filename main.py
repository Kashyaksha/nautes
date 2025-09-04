"""
Точка входа приложения.
Создаёт таблицы в БД (если нужно) и запускает Telegram-поллинг.
"""
from app.services.database import init_db
from app.telegram.telegram_bot import run
from app.utils.logger import logger

if __name__ == "__main__":
    logger.info("Инициализация базы данных...")
    init_db()  # создаёт таблицы и добавляет тестовые данные при первом запуске
    logger.info("Запуск Telegram-бота...")
    run()