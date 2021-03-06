import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True

    PROJECT_NAME: str = 'Movie together API'
    PROJECT_HOST: str = '0.0.0.0'
    PROJECT_PORT: int = 8000
    PROJECT_PROTOCOL: str = 'http'

    DB_HOST: str
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str

    KAFKA_HOST: str = os.getenv('KAFKA_HOST', 'kafka')
    KAFKA_PORT: int = 29092
    KAFKA_AUTO_COMMIT: bool = False
    KAFKA_AUTO_OFFSET_RESET: str = 'earliest'
    KAFKA_TOPIC: str = 'watch_together'

    AUTH_SERVICE_SCHEMA: str = 'http'
    AUTH_SERVICE_HOST: str = os.getenv('AUTH_SERVICE_HOST', 'auth')
    AUTH_SERVICE_PORT: int = os.getenv('AUTH_SERVICE_PORT', 80)
    AUTH_SERVICE_API_ENDPOINT: str = 'api'
    AUTH_SERVICE_V1_ENDPOINT: str = 'v1'
    AUTH_SERVICE_GET_ME_ENDPOINT: str = 'me'
    AUTHORIZATION_HEADER_NAME: str = 'authorization'

    JWT_SECRET_KEY: str
    JWT_ALG: str

    SENTRY_DSN: str

    @property
    def auth_service_url(self):
        return f'{self.AUTH_SERVICE_SCHEMA}://{self.AUTH_SERVICE_HOST}:{self.AUTH_SERVICE_PORT}'

    @property
    def pg_dsn(self):
        return f'postgresql+asyncpg://' \
               f'{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'  # noqa

    @property
    def kafka_config(self):
        return {
            'bootstrap_servers': f"{self.KAFKA_HOST}:{self.KAFKA_PORT}",
            'enable_auto_commit': self.KAFKA_AUTO_COMMIT,
            'auto_offset_reset': self.KAFKA_AUTO_OFFSET_RESET,
        }

    @property
    def get_root_url(self):
        return f'{self.PROJECT_PROTOCOL}://{self.PROJECT_HOST}:{self.PROJECT_PORT}'

    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()
