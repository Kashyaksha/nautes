"""
Telegram handlers: команды и callback query.
Все исключения ловим и логируем, чтобы TeleBot не падал.
"""
import html
from telebot import types
from telebot.types import Message, CallbackQuery

from app.core.base_bot import bot
from app.utils.logger import logger
from app.core import use_cases


# /start
@bot.message_handler(commands=["start"])
def cmd_start(message: Message):
    try:
        user = use_cases.get_or_create_user(message.from_user)

        text = (
            f"Привет, {message.from_user.first_name or 'гость'}!\n"
            "Я – путеводитель по городу 🌆.\n"
            "Можешь спросить меня:\n"
            "• где поесть 🍔\n"
            "• что посмотреть 🎭\n"
            "• куда сходить вечером 🎶\n\n"
            "Просто напиши свой запрос!"
        )

        bot.send_message(message.chat.id, text, parse_mode=None)

    except Exception as e:
        logger.exception("Error in /start handler")
        bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте ещё раз.")


# /help
@bot.message_handler(commands=["help"])
def cmd_help(message: Message):
    try:
        text = "Используй /categories или /search <запрос>. Также можно отправить локацию 📍"
        bot.send_message(message.chat.id, text, parse_mode=None)
    except Exception:
        logger.exception("Error in /help")
        bot.send_message(message.chat.id, "Ошибка команды /help")


# /categories
@bot.message_handler(commands=["categories"])
def cmd_categories(message: Message):
    try:
        cats = use_cases.list_categories()
        if not cats:
            bot.send_message(message.chat.id, "Категории пока не добавлены.")
            return

        markup = types.InlineKeyboardMarkup()
        for c in cats:
            markup.add(types.InlineKeyboardButton(text=c.name, callback_data=f"cat:{c.id}"))
        bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)
    except Exception:
        logger.exception("Error in /categories")
        bot.send_message(message.chat.id, "Не удалось загрузить категории.")


# /search
@bot.message_handler(commands=["search"])
def cmd_search(message: Message):
    try:
        args = message.text.partition(" ")[2].strip()
        if not args:
            bot.send_message(message.chat.id, "Использование: /search <запрос>")
            return

        results = use_cases.search_places(args)
        if not results:
            bot.send_message(message.chat.id, "Ничего не найдено.")
            return

        for p in results[:10]:
            text = f"<b>{html.escape(p.name)}</b>\n"
            if p.address:
                text += html.escape(p.address) + "\n"
            if p.description:
                text += html.escape(p.description[:200])

            kb = types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton("Подробнее", callback_data=f"place:{p.id}"))
            bot.send_message(message.chat.id, text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        logger.exception("Error in /search")
        bot.send_message(message.chat.id, "Ошибка поиска. Попробуй позднее.")


# Обработка callback (категории / места / избранное)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: CallbackQuery):
    try:
        data = call.data or ""
        if data.startswith("cat:"):
            cat_id = int(data.split(":")[1])
            places = use_cases.get_places_by_category(cat_id)
            if not places:
                bot.answer_callback_query(call.id, "Места в этой категории не найдены.")
                return

            text = f"Места в категории ({len(places)}):"
            kb = types.InlineKeyboardMarkup()
            for p in places[:20]:
                kb.add(types.InlineKeyboardButton(p.name, callback_data=f"place:{p.id}"))
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=text,
                                  reply_markup=kb)

        elif data.startswith("place:"):
            place_id = int(data.split(":")[1])
            p = use_cases.get_place(place_id)
            if not p:
                bot.answer_callback_query(call.id, "Место не найдено.")
                return

            parts = [f"<b>{html.escape(p.name)}</b>"]
            if p.address:
                parts.append(f"📍 {html.escape(p.address)}")
            if p.description:
                parts.append(html.escape(p.description))
            if p.category:
                parts.append(f"Категория: {html.escape(p.category.name)}")
            text = "\n\n".join(parts)

            kb = types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton("Добавить в избранное", callback_data=f"fav_add:{p.id}"))
            kb.add(types.InlineKeyboardButton("Поделиться", switch_inline_query=p.name))
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=text,
                                  reply_markup=kb,
                                  parse_mode="HTML")

        elif data.startswith("fav_add:"):
            place_id = int(data.split(":")[1])
            user = use_cases.get_or_create_user(call.from_user)
            use_cases.add_favorite(user.id, place_id)
            bot.answer_callback_query(call.id, "Добавлено в избранное ✅")

        else:
            bot.answer_callback_query(call.id, "Неизвестная команда.")

    except Exception:
        logger.exception("Error in callback handler")
        try:
            bot.answer_callback_query(call.id, "Ошибка обработки запроса.")
        except Exception:
            pass


# Эхо (fallback)
@bot.message_handler(func=lambda m: True)
def fallback_echo(message: Message):
    try:
        if message.location:
            bot.send_message(message.chat.id, "Спасибо за локацию! Скоро я научусь искать заведения рядом 🗺️")
            return
        bot.send_message(message.chat.id, f"Ты написал: {message.text}\n\nИспользуй /help для списка команд.")
    except Exception:
        logger.exception("Error in fallback handler")
