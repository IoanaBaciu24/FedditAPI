from typing import Dict
from nltk.sentiment import SentimentIntensityAnalyzer
from app.core.constants import SENTIMENT

_analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(comment_id: str, text: str) -> Dict[str, str | float]:
    """
    Analyze the sentiment of a comment.

    Args:
        comment_id (str): Unique identifier of the comment.
        text (str): Text content of the comment.

    Returns:
        dict: A dictionary with:
            - id (str): the comment ID
            - text (str): the original comment text
            - polarity (float): sentiment score from -1 (neg) to +1 (pos)
            - sentiment (str): "positive" or "negative" based on polarity
    """
    score = _analyzer.polarity_scores(text)["compound"]
    sentiment = SENTIMENT.POSITIVE if score >= 0 else SENTIMENT.NEGATIVE

    return {
        SENTIMENT.ID: comment_id,
        SENTIMENT.TEXT: text,
        SENTIMENT.SCORE: round(score, 4),
        SENTIMENT.SENTIMENT: sentiment,
    }
