from __future__ import annotations
from typing import Literal, Optional, Tuple
from fuzzywuzzy import fuzz

# Простейший классификатор запроса
def classify_text(text: str) -> Tuple[str, Optional[str]]:
    """Возвращает (intent, arg). Примеры intent: 'search', 'category', 'help'."""
    t = (text or '').strip().lower()
    if not t:
        return ("help", None)
    if t.startswith(('/start', 'start', 'help', '/help')):
        return ("help", None)

    # Простые эвристики
    for key in ('кафе', 'ресторан', 'музей', 'кино', 'больница', 'поликлиника', 'аптека'):
        if key in t:
            return ("category", key)

    # Если похоже на команду "найди ..."
    if t.startswith(("найди", "ищи", "поищи")):
        arg = t.split(" ", 1)[1] if " " in t else ""
        return ("search", arg)

    # В противном случае — свободный поиск по названию
    return ("search", t)

def short_help() -> str:
    return (
        "Я помогу найти места в городе: попробуй 'кафе', 'музей' или напиши 'найди Кафе Central'.\n"
        "Команды: /start — приветствие, /help — помощь."
    )
