import logging
from logging.config import fileConfig

import urls
from aiohttp import web
from config import settings

fileConfig(settings.LOGGING_CONFIG_FILE)
logger = logging.getLogger("ugc")

POST_METHOD = "POST"


async def views_handler(request):
    data = await request.json()
    logger.info(
        f"Film View: movie_id: {data}"
    )
    return web.Response(text="Got film view event data")


async def reviews_handler(request):
    data = await request.json()
    logger.info(
        f"Review: movie_id: {data}"
    )
    return web.Response(text="Got new review data")


async def film_like_handler(request):
    data = await request.json()
    logger.info(f"Film like: {data}")
    return web.Response(text="Got new film like")


async def review_like_handler(request):
    data = await request.json()
    logger.info(
        f"Review like: {data}"
    )
    return web.Response(text="Got new review like")


async def bookmark_handler(request):
    data = await request.json()
    logger.info(f"Bookmark: {data}")
    return web.Response(text="Got new bookmark")


if __name__ == "__main__":
    app = web.Application()
    app.router.add_route(POST_METHOD, urls.urlpatterns[urls.DataType.VIEW.value], views_handler)
    app.router.add_route(
        POST_METHOD, urls.urlpatterns[urls.DataType.REVIEW.value], reviews_handler
    )
    app.router.add_route(
        POST_METHOD, urls.urlpatterns[urls.DataType.FILM_LIKE.value], film_like_handler
    )
    app.router.add_route(
        POST_METHOD, urls.urlpatterns[urls.DataType.REVIEW_LIKE.value], review_like_handler
    )
    app.router.add_route(
        POST_METHOD, urls.urlpatterns[urls.DataType.BOOKMARK.value], bookmark_handler
    )
    web.run_app(app)
