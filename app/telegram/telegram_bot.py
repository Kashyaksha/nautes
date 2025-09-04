from app.core.base_bot import bot
import app.core.handlers  # noqa: F401 - регистрируем хендлеры
from app.utils.logger import logger
import time

def run():
    """
    Запуск бота. Infinity polling внутри — ловим исключения,
    чтобы бот автоматически рестартовал при нефатальных ошибках.
    """
    while True:
        try:
            logger.info("Bot polling started (skip_pending=True)")
            bot.infinity_polling(skip_pending=True)
        except Exception as e:
            logger.exception("Bot polling crashed: %s", e)
            logger.info("Restarting polling in 5 seconds...")
            time.sleep(5)
