import re
from exceptions import InvalidInputError

def find_longest_word(text: str):
    if not isinstance(text, str):
        raise InvalidInputError("Нечего обрабатывать")
    if not text.strip():
        raise InvalidInputError("Нечего обрабатывать")
    words = re.findall(r'\b\w+\b', text)
    if not words:
        return [],0
    max_len = max(len(w) for w in words)
    longest_word = list(dict.fromkeys(w for w in words if len(w) == max_len))
    return longest_word, max_len