"""
Простая функция поиска / классификации текста.
Здесь можно потом подключить более мощные модели.
"""
from difflib import get_close_matches
from typing import List

def fuzzy_match(query: str, choices: List[str], n: int = 3) -> List[str]:
    """
    Возвращает лучшие совпадения (difflib).
    """
    return get_close_matches(query, choices, n=n, cutoff=0.5)
