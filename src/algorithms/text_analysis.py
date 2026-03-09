from __future__ import annotations

from src.algorithms.helpers import get_unique_words, is_prime


def analyze_texts(texts: list[str]) -> dict:
    """Analyze a list of texts and return stats about word frequencies.

    Returns a dict with:
    - word_counts: dict mapping each unique word to its total count across all texts
    - prime_count_words: list of words whose total count is a prime number
    - top_words: the top 10 most frequent words, sorted by count descending
    """
    word_counts: dict[str, int] = {}

    for text in texts:
        for word in text.lower().split():
            cleaned = "".join(filter(str.isalnum, word))
            if cleaned:
                word_counts[cleaned] = word_counts.get(cleaned, 0) + 1

    prime_count_words = sorted(
        [word for word, count in word_counts.items() if is_prime(count)]
    )

    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    top_words = sorted_words[:10]

    return {
        "word_counts": word_counts,
        "prime_count_words": prime_count_words,
        "top_words": top_words,
    }
