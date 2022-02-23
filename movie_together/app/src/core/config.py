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

    @property
    def pg_dsn(self):
        return f'postgresql+asyncpg://' \
               f'{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'  # noqa

    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()
