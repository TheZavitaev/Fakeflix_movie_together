from pydantic import BaseSettings

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = 'UGC API'
    PROJECT_DESCRIPTION: str = 'API для записи пользовательского контента'
    API_VERSION = '1.0.0'

    kafka_host: str = 'kafka:9092'
    kafka_movie_progress_topic: str = 'movie_progress'

    api_host: str = '0.0.0.0'  # noqa: S104
    api_port: int = 8000

    MONGO_DSN: str
    MONGO_DATABASE: str = 'movie'
    MONGO_COLLECTION_LIKE: str = 'like'
    MONGO_COLLECTION_BOOKMARK: str = 'bookmark'
    MONGO_COLLECTION_REVIEW: str = 'review'
    MONGO_COLLECTION_REVIEW_RATING: str = 'review_rating'
    MONGO_COLLECTION_MOVIES: str = 'movies'

    PAGE_SIZE: int = 3

    sentry_dsn: str

    logstash_host: str = 'logstash'
    logstash_port: int = 5044

    class Config:  # noqa: WPS431
        env_file = ".env"


settings = Settings()
