import pytest
from unittest.mock import AsyncMock, patch
from app.endpoints import get_id_for_subfeddit_title, get_comments_from_id
from app.core.constants import CONF, FEDDIT

@pytest.fixture
def config():
    return {
        CONF.BASE_URL: "https://fake-feddit.api",
        CONF.SUBFEDDITS: "subfeddits",
        CONF.COMMENTS: "comments"
    }

@pytest.mark.asyncio
async def test_get_id_for_subfeddit_title_found(config):
    mock_data = [
        {FEDDIT.ID: "1", FEDDIT.TITLE: "funny"},
        {FEDDIT.ID: "2", FEDDIT.TITLE: "news"},
    ]

    with patch("httpx.AsyncClient.get", new=AsyncMock(return_value=AsyncMock(json=lambda: mock_data, raise_for_status=lambda: None))):
        result = await get_id_for_subfeddit_title("funny", config)
        assert result == "1"

@pytest.mark.asyncio
async def test_get_id_for_subfeddit_title_not_found(config):
    mock_data = [
        {FEDDIT.ID: "1", FEDDIT.TITLE: "funny"},
    ]

    with patch("httpx.AsyncClient.get", new=AsyncMock(return_value=AsyncMock(json=lambda: mock_data, raise_for_status=lambda: None))):
        result = await get_id_for_subfeddit_title("nonexistent", config)
        assert result is None

@pytest.mark.asyncio
async def test_get_comments_from_id(config):
    mock_comments = {
        FEDDIT.COMMENTS: [
            {"id": "1", "text": "Nice post"},
            {"id": "2", "text": "Terrible opinion"}
        ]
    }

    with patch("httpx.AsyncClient.get", new=AsyncMock(return_value=AsyncMock(json=lambda: mock_comments, raise_for_status=lambda: None))):
        result = await get_comments_from_id("1", config)
        assert isinstance(result, list)
        assert result[0]["id"] == "1"
        assert result[1]["text"] == "Terrible opinion"
