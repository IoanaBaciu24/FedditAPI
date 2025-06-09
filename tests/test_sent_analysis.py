from app.sentiment_analysis import analyze_sentiment
from app.core.constants import SENTIMENT


def test_positive_sentiment():
    result = analyze_sentiment("1", "I love this!")
    assert result[SENTIMENT.SENTIMENT] == SENTIMENT.POSITIVE
    assert result[SENTIMENT.SCORE] > 0


def test_negative_sentiment():
    result = analyze_sentiment("2", "This is terrible.")
    assert result[SENTIMENT.SENTIMENT] == SENTIMENT.NEGATIVE
    assert result[SENTIMENT.SCORE] < 0
