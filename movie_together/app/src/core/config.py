from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True

    PROJECT_NAME: str = 'Movie together API'
    PROJECT_HOST: str = '0.0.0.0'
    PROJECT_PORT: int = 8000

    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USERNAME: str = 'postgres'
    DB_PASSWORD: str = 'postgres'
    DB_NAME: str = 'postgres'

    KAFKA_HOST: str = 'kafka'
    KAFKA_PORT: int = 29092
    KAFKA_AUTO_COMMIT: bool = False
    KAFKA_AUTO_OFFSET_RESET: str = 'earliest'
    KAFKA_TOPIC: str = 'watch_together'

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

    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()
