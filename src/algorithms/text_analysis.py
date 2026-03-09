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
        unique_words = get_unique_words(text)
        all_words = []
        for word in text.lower().split():
            cleaned = ""
            for ch in word:
                if ch.isalnum():
                    cleaned += ch
            if cleaned:
                all_words.append(cleaned)

        for word in all_words:
            if word in unique_words:
                if word in word_counts:
                    word_counts[word] = word_counts[word] + 1
                else:
                    word_counts[word] = 1

    prime_count_words = []
    for word, count in word_counts.items():
        if is_prime(count):
            prime_count_words.append(word)
    prime_count_words.sort()

    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    top_words = []
    for i in range(min(10, len(sorted_words))):
        top_words.append(sorted_words[i])

    return {
        "word_counts": word_counts,
        "prime_count_words": prime_count_words,
        "top_words": top_words,
    }