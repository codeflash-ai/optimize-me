from __future__ import annotations


def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def get_unique_words(text: str) -> list[str]:
    """Return sorted unique words from text, ignoring case."""
    words = text.lower().split()
    unique = []
    for word in words:
        cleaned = ""
        for ch in word:
            if ch.isalnum():
                cleaned += ch
        if cleaned and cleaned not in unique:
            unique.append(cleaned)
    unique.sort()
    return unique
