import logging

import sentry_sdk
import uvicorn
from api.v1 import movie, movie_progress, user
from core.config import settings
from core.logger import LOGGING, RequestIdFilter
from db import kafka, mongodb
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from logstash_async.handler import AsynchronousLogstashHandler
from motor.motor_asyncio import AsyncIOMotorClient
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

sentry_sdk.init(dsn=settings.sentry_dsn)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url='/api/v1/openapi',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
)

app.add_middleware(SentryAsgiMiddleware)


logger = logging.getLogger(__name__)
handler = AsynchronousLogstashHandler(
    settings.logstash_host,
    settings.logstash_port,
    transport="logstash_async.transport.UdpTransport",
    database_path="logstash.db",
    version=1
)

logger.addFilter(RequestIdFilter())
logger.addHandler(handler)


@app.on_event('startup')
async def startup_event():
    kafka.kafka_producer = kafka.AsyncKafkaProducer(settings.kafka_host)
    await kafka.kafka_producer.start_producer()

    client = AsyncIOMotorClient(settings.MONGO_DSN)
    mongodb.mongodb_engine = client


@app.on_event('shutdown')
async def shutdown_event():
    await kafka.kafka_producer.stop_producer()


app.include_router(movie_progress.router, prefix='/api/v1/movie-progress', tags=['movie-progress'])
app.include_router(user.router, prefix='/api/v1/users', tags=['user'])
app.include_router(movie.router, prefix='/api/v1/movies', tags=['movie'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.api_host,
        port=settings.api_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
