import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from unittest.mock import patch

from app.core.constants import SENTIMENT

from app.main import app


@pytest.mark.asyncio
@patch("app.main.get_comments_from_id")
@patch("app.main.get_id_for_subfeddit_title")
async def test_analyze_endpoint(mock_get_id, mock_get_comments):
    mock_get_id.return_value = "s1"
    mock_get_comments.return_value = [
        {SENTIMENT.ID: "c1", SENTIMENT.TEXT: "I love this!"},
        {SENTIMENT.ID: "c2", SENTIMENT.TEXT: "This is terrible."},
    ]

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        response = await async_client.get("/analyze?title=funny&limit=2")

    assert response.status_code == status.HTTP_200_OK
    results = response.json()
    assert len(results) == 2

    assert results[0][SENTIMENT.ID] == "c1"
    assert results[0][SENTIMENT.SENTIMENT] == SENTIMENT.POSITIVE
    assert results[1][SENTIMENT.ID] == "c2"
    assert results[1][SENTIMENT.SENTIMENT] == SENTIMENT.NEGATIVE
