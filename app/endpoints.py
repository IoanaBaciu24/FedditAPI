import httpx
from app.core.config import Config
from app.core.constants import CONF, FEDDIT


async def get_id_for_subfeddit_title(title: str, config: Config) -> str:
    """
    Asynchronously fetch the ID of a subfeddit by its title.

    Args:
        title (str): The title of the subfeddit to search for.
        config (Config): The configuration object containing API settings.

    Returns:
        str: The ID of the subfeddit if found, otherwise None.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{config[CONF.BASE_URL]}/{config[CONF.SUBFEDDITS]}"
        )
        response.raise_for_status()
        data = response.json()
        return next(
            (item[FEDDIT.ID] for item in data if item[FEDDIT.TITLE] == title), None
        )


async def get_comments_from_id(id: str, config: Config, skip: int = 0, limit: int = 25):
    """
    Asynchronously fetch comments for a given subfeddit ID.

    Args:
        id (str): The ID of the subfeddit to fetch comments from.
        config (Config): The configuration object containing API settings.
        skip (int, optional): The number of comments to skip (for pagination). Defaults to 0.
        limit (int, optional): The maximum number of comments to return. Defaults to 25.

    Returns:
        list: A list of comments associated with the subfeddit ID.
    """
    async with httpx.AsyncClient() as client:
        url = (
            f"{config[CONF.BASE_URL]}/{config[CONF.COMMENTS]}/"
            f"?{FEDDIT.SUBFEDDIT_ID}={id}"
            f"&{FEDDIT.LIMIT}={limit}"
            f"&{FEDDIT.SKIP}={skip}"
        )
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        return data[FEDDIT.COMMENTS]
