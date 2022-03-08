import logging
from logging import config as logging_config

import sentry_sdk
import uvicorn as uvicorn
from fastapi import FastAPI, Security
from fastapi.responses import ORJSONResponse
from fastapi.security import APIKeyHeader
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.middleware.authentication import AuthenticationMiddleware

from api.routers import api_router
from core.auth.middleware import CustomAuthBackend
from core.config import settings
from core.logger import LOGGING
from db import postgres


logging_config.dictConfig(LOGGING)

api_key = APIKeyHeader(name='authorization', auto_error=False)

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

# Include API router
app.include_router(
    api_router,
    prefix='/api',
    dependencies=[Security(api_key)],
)

# Activate auth middleware
app.add_middleware(AuthenticationMiddleware, backend=CustomAuthBackend())

# Initiate Sentry
sentry_sdk.init(
    dsn=settings.SENTRY_DSN
)
asgi_app = SentryAsgiMiddleware(app)
app.add_middleware(SentryAsgiMiddleware)


@app.on_event('startup')
async def startup():
    postgres.async_pg_engine = create_async_engine(settings.pg_dsn, echo=True)


@app.on_event('shutdown')
async def shutdown():
    await postgres.async_pg_engine.dispose()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.PROJECT_HOST,
        port=settings.PROJECT_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=settings.DEBUG,
    )
