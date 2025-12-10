import re
from collections import Counter
from exceptions import InvalidInputError

def find_unique_words(text: str) -> list[str]:
    if not isinstance(text, str):
        raise InvalidInputError("Входной текст должен быть строкой")
    if not text.strip:
        raise InvalidInputError("Текст пустой")
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    return [word for word, count in word_counts.items() if count == 1]