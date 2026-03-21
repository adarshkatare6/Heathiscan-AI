from __future__ import annotations

import re
from typing import Set

import nltk
from nltk.corpus import stopwords


_FALLBACK_STOPWORDS: Set[str] = {
    # Minimal fallback if nltk data is unavailable in the runtime environment.
    "the",
    "a",
    "an",
    "and",
    "or",
    "but",
    "if",
    "then",
    "else",
    "with",
    "without",
    "of",
    "to",
    "in",
    "for",
    "on",
    "at",
    "by",
    "from",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "it",
    "this",
    "that",
    "these",
    "those",
    "as",
    "i",
    "you",
    "he",
    "she",
    "they",
    "we",
    "them",
    "us",
    "my",
    "your",
    "our",
    "their",
    "but",
    "not",
    "no",
    "yes",
}

_STOP_WORDS_CACHE: Set[str] | None = None


def _ensure_stopwords_loaded() -> Set[str]:
    """
    Load NLTK stopwords. If the runtime has no internet or downloads are blocked,
    fall back to a small built-in stopword set.
    """
    global _STOP_WORDS_CACHE
    if _STOP_WORDS_CACHE is not None:
        return _STOP_WORDS_CACHE

    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        try:
            nltk.download("stopwords", quiet=True)
        except Exception:
            _STOP_WORDS_CACHE = _FALLBACK_STOPWORDS
            return _STOP_WORDS_CACHE

    try:
        _STOP_WORDS_CACHE = set(stopwords.words("english"))
        return _STOP_WORDS_CACHE
    except Exception:
        _STOP_WORDS_CACHE = _FALLBACK_STOPWORDS
        return _STOP_WORDS_CACHE


def clean_text(text: str) -> str:
    """
    Clean OCR text:
    - lowercase
    - remove special characters and numbers
    - remove stopwords (nltk)
    - normalize spaces
    """
    if text is None:
        return ""

    text = str(text).lower()

    # Remove digits (numbers) first.
    text = re.sub(r"\d+", " ", text)

    # Keep letters and spaces; convert punctuation/symbols to spaces.
    text = re.sub(r"[^a-z\s]", " ", text)

    # Collapse whitespace early to keep tokenization clean.
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return ""

    stop_words = _ensure_stopwords_loaded()
    tokens = [tok for tok in text.split() if tok and tok not in stop_words]
    cleaned = " ".join(tokens)

    # Final whitespace normalization.
    return re.sub(r"\s+", " ", cleaned).strip()

