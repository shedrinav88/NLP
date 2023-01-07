from enum import Enum
import config
import logging
from typing import Union
from aiohttp import ClientSession, TCPConnector

logger = logging.getLogger(__name__)


class KinopoiskType(Enum):
    search_film = "search_film"
    search_actors = "search_actors"
    get_actor = "get_actor"


async def search_kinopoisk(type: KinopoiskType, search_string: str) -> Union[dict, None]:
    try:
        if type == KinopoiskType.search_film:
            url = f"https://api.kinopoisk.dev/movie?token={config.kinopoisk_token}&search={search_string}&field=name&isStrict=false"
        elif type == KinopoiskType.search_actors:
            url = f"https://api.kinopoisk.dev/person?token={config.kinopoisk_token}&search={search_string}&field=name&isStrict=false"
        elif type == KinopoiskType.get_actor:
            url = f"https://api.kinopoisk.dev/person?token={config.kinopoisk_token}&search={search_string}&field=id"
        else:
            return None
        async with ClientSession(connector=TCPConnector(verify_ssl=False)) as sess:
            response = await sess.get(url)
            return await response.json()
    except Exception as err:
        logger.error(f'Can\'t get movie data. {err}')
        return None
