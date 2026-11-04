from news_analysis.preprocess import preprocess_text
from news_analysis.schema import normalize_newsapi_article, polarity_label


def test_preprocess_is_deterministic():
    assert preprocess_text("Apple earnings are beating expectations") == preprocess_text(
        "Apple earnings are beating expectations"
    )


def test_polarity_label():
    assert polarity_label(1) == "Positive"
    assert polarity_label(0) == "Neutral"
    assert polarity_label(-1) == "Negative"


def test_normalization_keeps_iso_date_and_ticker():
    document = normalize_newsapi_article(
        {
            "title": "Apple rises",
            "description": "Shares gain",
            "url": "https://example.com/a",
            "publishedAt": "2026-01-01T10:00:00Z",
        },
        ticker="AAPL",
        analysis={"is_business": 1, "polarity": 1, "polarity_label": "Positive"},
    )
    assert document["ticker"] == "$AAPL"
    assert document["publishedAt"] == "2026-01-01T10:00:00Z"
    assert document["prediction"] == "Positive"
    assert document["polarity_score"] == 1
