"""Deterministic, offline text preprocessing shared by training and serving.

The original 2022 notebook used NLTK's stopword corpus.  The list below is the
scikit-learn English stopword list, which lets the restored pipeline train and
serve without downloading NLTK data.  Porter stemming is kept from the original
notebook because it is part of the model's preprocessing contract.
"""

from __future__ import annotations

from functools import lru_cache

from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

_STOPWORDS = frozenset(ENGLISH_STOP_WORDS)


@lru_cache(maxsize=1)
def _stemmer() -> PorterStemmer:
    return PorterStemmer()


def preprocess_text(text: str) -> str:
    """Lowercase, tokenize, remove stopwords and apply Porter stemming."""
    if not isinstance(text, str):
        return ""
    stem = _stemmer().stem
    tokens = [stem(word) for word in text.lower().split() if word not in _STOPWORDS]
    return " ".join(tokens)


# Kept for compatibility with the original notebook/service naming.
def text_transformer(text: str) -> list[str]:
    return [preprocess_text(text)]
