from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
from app.sentiment_analysis import analyze_sentiment
from app.core.config import Config
from app.core.constants import FEDDIT, SENTIMENT
from app.endpoints import get_id_for_subfeddit_title, get_comments_from_id

app = FastAPI()
config = Config()


@app.get("/analyze", summary="Analyze comments for a subfeddit")
async def analyze_subfeddit_comments(
    title: str = Query(..., description="Title of the subfeddit"),
    limit: int = Query(
        25, le=100, description="Max number of comments to return (default 25)"
    ),
    sort_by_score: bool = Query(
        False, description="Query over wether we want the comments sorted."
    ),
    start_date: Optional[datetime] = Query(
        None, description="Start date in ISO format"
    ),
    end_date: Optional[datetime] = Query(None, description="End date in ISO format"),
):
    subfeddit_id = await get_id_for_subfeddit_title(title, config)
    if not subfeddit_id:
        raise HTTPException(status_code=404, detail="Subfeddit not found")

    comments = await get_comments_from_id(subfeddit_id, config, limit=limit)

    analyzed = [
        analyze_sentiment(comment[FEDDIT.ID], comment[FEDDIT.TEXT])
        for comment in comments
    ]

    if start_date or end_date:

        def in_range(comment):
            ts = comment.get(FEDDIT.TIMESTAMP)
            if ts is None:
                return False
            try:
                dt = datetime.fromtimestamp(ts)
            except (TypeError, ValueError):
                return False
            return (not start_date or dt >= start_date) and (
                not end_date or dt <= end_date
            )

        analyzed = [c for c, c_ts in zip(analyzed, comments) if in_range(c_ts)]
    if sort_by_score:
        analyzed.sort(key=lambda x: x[SENTIMENT.SCORE], reverse=True)
    return analyzed
