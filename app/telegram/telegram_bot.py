from __future__ import annotations
from typing import List
from telebot.types import Message
from telebot import apihelper
from app.services.messenger import get_bot
from app.services.database import SessionLocal, search_places, search_by_category, Place
from app.services import database as db
from app.services.nlp import classify_text, short_help
from app.utils.logger import logger

bot = get_bot()

@bot.message_handler(commands=['start', 'help'])
def cmd_start(message: Message):
    bot.reply_to(message, "Привет! Я подскажу места и организации в городе.\n" + short_help())

@bot.message_handler(content_types=['text'])
def on_text(message: Message):
    text = (message.text or '').strip()
    intent, arg = classify_text(text)
    logger.info("intent=%s arg=%s text=%s", intent, arg, text)
    with SessionLocal() as session:
        if intent == 'help':
            bot.reply_to(message, short_help())
            return
        if intent == 'category' and arg:
            res = search_by_category(session, arg)
            if not res:
                bot.reply_to(message, f"Не нашёл по категории '{arg}'. Попробуйте по названию.")
            else:
                bot.reply_to(message, format_places(res))
            return
        if intent == 'search' and arg:
            res = search_places(session, arg)
            if not res:
                bot.reply_to(message, f"Не нашёл '{arg}'. Попробуйте иначе или укажите категорию.")
            else:
                bot.reply_to(message, format_places(res))
            return
        bot.reply_to(message, short_help())

def format_places(pls: List[Place]) -> str:
    lines = []
    for p in pls:
        line = f"• <b>{p.name}</b> — {p.category}"
        if p.address: line += f" | {p.address}"
        if p.phone: line += f" | {p.phone}"
        lines.append(line)
    return "\n".join(lines) or "Ничего не найдено."

def run() -> None:
    logger.info("Старт поллинга Telegram...")
    bot.infinity_polling(skip_pending=True, allowed_updates=["message"])
