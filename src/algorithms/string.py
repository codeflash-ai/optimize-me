from __future__ import annotations

import re


def string_concat(n):
    s = ""
    for i in range(n):
        s += str(i)
    return s


def regex_match(strings: list[str], pattern: str) -> list[str]:
    matched = []
    for s in strings:
        if re.match(pattern, s):
            matched.append(s)
    return matched


def is_palindrome(text: str) -> bool:
    cleaned_text = "".join(c.lower() for c in text if c.isalnum())
    for i in range(len(cleaned_text) // 2):
        if cleaned_text[i] != cleaned_text[len(cleaned_text) - 1 - i]:
            return False
    return True


def word_frequency(text: str) -> dict[str, int]:
    words = text.lower().split()
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency


def find_common_tags(articles: list[dict[str, list[str]]]) -> set[str]:
    if not articles:
        return set()

    # Find the article with the smallest tags list to initialize common_tags
    min_idx = 0
    min_len = len(articles[0].get("tags", []))
    if min_len == 0:
        return set()

    for i in range(1, len(articles)):
        tags_i = articles[i].get("tags", [])
        li = len(tags_i)
        if li < min_len:
            min_len = li
            min_idx = i
            if min_len == 0:
                return set()

    common_tags = set(articles[min_idx].get("tags", []))
    # Iterate over all articles except the one used to initialize common_tags
    for i in range(len(articles)):
        if i == min_idx:
            continue
        common_tags.intersection_update(articles[i].get("tags", []))
        if not common_tags:
            break
    return common_tags
