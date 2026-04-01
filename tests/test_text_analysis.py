from src.algorithms.text_analysis import analyze_texts


def test_analyze_texts_basic() -> None:
    texts = [
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox is very quick",
        "A lazy dog sleeps all day",
    ]
    result = analyze_texts(texts)

    assert result["word_counts"]["the"] == 3
    assert result["word_counts"]["quick"] == 3
    assert result["word_counts"]["fox"] == 2
    assert "quick" in result["prime_count_words"]  # 3 is prime
    assert "fox" in result["prime_count_words"]  # 2 is prime
    assert "the" in result["prime_count_words"]  # 3 is prime
    assert result["top_words"][0][1] >= result["top_words"][1][1]


def test_analyze_texts_empty() -> None:
    result = analyze_texts([])
    assert result["word_counts"] == {}
    assert result["prime_count_words"] == []
    assert result["top_words"] == []


def test_analyze_texts_single_text() -> None:
    texts = ["hello world hello world hello"]
    result = analyze_texts(texts)
    assert result["word_counts"]["hello"] == 3
    assert result["word_counts"]["world"] == 2
    assert "hello" in result["prime_count_words"]  # 3 is prime
    assert "world" in result["prime_count_words"]  # 2 is prime