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

    # Pre-extract tag lists to avoid repeated .get lookups and slicing overhead
    tag_lists = [article.get("tags", []) for article in articles]
    # Sort by length to intersect smaller sets first (reducing intersection cost)
    tag_lists.sort(key=len)
    # Early return if any are empty
    if not tag_lists[0]:
        return set()
    # Build initial set from smallest tag list
    common_tags = set(tag_lists[0])
    for tags in tag_lists[1:]:
        common_tags.intersection_update(tags)
        if not common_tags:
            break
    return common_tags
