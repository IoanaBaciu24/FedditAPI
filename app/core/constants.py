class CONF:
    BASE_URL = "base_url"
    SUBFEDDITS = "subfeddits_url"
    SUBFEDDIT = "subfeddit_url"
    COMMENTS = "comments_url"


class FEDDIT:
    ID = "id"
    TITLE = "title"
    SUBFEDDIT_ID = "subfeddit_id"
    LIMIT = "limit"
    SKIP = "skip"
    COMMENTS = "comments"
    SUBFEDDITS = "subfeddits"

    TEXT = "text"
    TIMESTAMP = "created_at"


class SENTIMENT:
    POSITIVE = "positive"
    NEGATIVE = "negative"

    ID = "id"
    TEXT = "text"
    SENTIMENT = "sentiment"
    SCORE = "score"
