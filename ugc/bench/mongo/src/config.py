from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    DB_NAME = 'ugc_db'

    BENCHMARK_ITERATIONS = 10


settings = Settings()
