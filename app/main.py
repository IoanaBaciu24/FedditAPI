from fastapi import FastAPI, HTTPException, Query

from app.sentiment_analysis import analyze_sentiment
from app.core.config import Config
from app.endpoints import get_id_for_subfeddit_title, get_comments_from_id

app = FastAPI()
config = Config()

@app.get("/analyze", summary="Analyze comments for a subfeddit")
async def analyze_subfeddit_comments(
    title: str = Query(..., description="Title of the subfeddit"),
    limit: int = Query(25, le=100, description="Max number of comments to return (default 25)")
):
    subfeddit_id = await get_id_for_subfeddit_title(title, config)
    if not subfeddit_id:
        raise HTTPException(status_code=404, detail="Subfeddit not found")

    comments = await get_comments_from_id(subfeddit_id, config, limit=limit)

    analyzed = [
        analyze_sentiment(comment["id"], comment["text"])
        for comment in comments
    ]

    return analyzed
