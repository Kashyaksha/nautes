from app.services.database import init_db
from app.telegram.telegram_bot import run


if __name__ == "__main__":
    init_db()  # создаёт таблицы, если их нет
    from app.core.base_bot import bot
    bot.infinity_polling()