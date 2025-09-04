"""
Отправка сообщений — одна точка для обёртки вызовов Telegram (в будущем можно подключить WhatsApp).
"""
from app.core.base_bot import bot
from app.utils.logger import logger
from telebot import types

def send_text(chat_id: int, text: str, reply_markup: types.InlineKeyboardMarkup = None):
    try:
        return bot.send_message(chat_id, text, reply_markup=reply_markup)
    except Exception as e:
        logger.exception("Failed to send message to %s: %s", chat_id, e)
        raise
