from app.core.base_bot import bot

def send_text(chat_id: int, text: str):
    return bot.send_message(chat_id, text)