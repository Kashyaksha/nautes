from app.core.base_bot import bot
# Импорт обработчиков важен, чтобы зарегистрировать хендлеры
import app.core.handlers # noqa: F401




def run():
    bot.infinity_polling(skip_pending=True)