from app.core.base_bot import bot
from app.services.database import get_session, User
from app.utils.helpers import safe_username


@bot.message_handler(commands=["start"])
def on_start(message):
    username = safe_username(message.from_user)
    with get_session() as s:
        user = s.query(User).filter(User.username == username).first()
        if not user:
            s.add(User(username=username))
    bot.reply_to(message, "Привет 👋 Я учебный бот Nautes. Напиши что-нибудь.")


@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, f"Ты написал: {message.text}")