import logging
import sys
import typing
from urllib.parse import urljoin

import aiohttp
import backoff
import urls
from config import settings
from urllib3.exceptions import MaxRetryError, NewConnectionError

import utils

logger = logging.getLogger("ugc")

STATUS_OK = 200

backoff_params = {
    "wait_gen": backoff.expo,
    "on_backoff": utils.backoff_hdlr,
    "factor": settings.BACKOFF_FACTOR,
    "max_value": settings.BACKOFF_MAX_WAIT,
    "exception": (
        aiohttp.ClientError,
        ConnectionRefusedError,
        MaxRetryError,
        NewConnectionError,
    ),
}


@backoff.on_exception(**backoff_params)
async def run_generator(datatype: str, max_batch_size: int, host: str) -> None:
    generator_class = getattr(sys.modules["producers"], f"{datatype.title()}Generator")
    stream = generator_class(max_batch_size).generate()
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        await _send_stream(stream, host, session)


async def _send_stream(
    stream: typing.Generator, host: str, session: aiohttp.ClientSession
) -> None:
    for batch in stream:
        for kind, item in batch:
            url = urljoin(host, urls.urlpatterns[kind])

            if kind == urls.DataType.REVIEW_LIKE.value:
                url = url.format(
                    user_id=item.pop("user_id"), review_id=item.pop("review_id")
                )
            elif kind in {urls.DataType.REVIEW.value, urls.DataType.FILM_LIKE.value, urls.DataType.BOOKMARK.value}:
                url = url.format(user_id=settings.API_JWT_USER)

            async with session.post(
                url, json=item, headers={"Authorization": f"Bearer {settings.API_JWT}"}
            ) as response:
                logger.info(response.status)
