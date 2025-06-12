import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from unittest.mock import patch

from app.core.constants import SENTIMENT, FEDDIT
from app.main import app


@pytest.mark.asyncio
@patch("app.main.get_comments_from_id")
@patch("app.main.get_id_for_subfeddit_title")
async def test_analyze_endpoint(mock_get_id, mock_get_comments):
    mock_get_id.return_value = "s1"
    mock_get_comments.return_value = [
        {
            FEDDIT.ID: "c1",
            FEDDIT.TEXT: "I love this!",
            FEDDIT.TIMESTAMP: 1695757477,  # 2023-09-26
        },
        {
            FEDDIT.ID: "c2",
            FEDDIT.TEXT: "This is terrible.",
            FEDDIT.TIMESTAMP: 1695843877,  # 2023-09-27
        },
    ]

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        response = await async_client.get(
            "/analyze?"
            "title=funny&"
            "limit=2&"
            "sort_by_score=true&"
            "start_date=2023-09-26&"
            "end_date=2023-09-28"
        )

    assert response.status_code == status.HTTP_200_OK
    results = response.json()
    assert len(results) == 2

    # Validate response format and sorting
    assert all(SENTIMENT.ID in r for r in results)
    assert all(SENTIMENT.SENTIMENT in r for r in results)
    assert all(SENTIMENT.SCORE in r for r in results)
    assert results[0][SENTIMENT.SCORE] >= results[1][SENTIMENT.SCORE]
