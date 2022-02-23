from pydantic import BaseSettings


class Settings(BaseSettings):
    API_JWT: str

    API_JWT_USER: str = "e7997aa5-0ef4-4bb8-bf7c-c893bc1d8b5f"
    FILM_MIN_LENGTH: int = 60 * 45  # noqa: WPS432
    FILM_MAX_LENGTH: int = 60 * 60 * 5  # noqa: WPS432
    LOGGING_CONFIG_FILE: str = "logging.ini"
    BATCH_INTERVAL: int = 1  # noqa: WPS432
    BACKOFF_FACTOR: float = 0.1  # noqa: WPS432
    BACKOFF_MAX_WAIT: int = 10  # noqa: WPS432
    UGC_API_URL: str = "/api/v1/movie-progress/"  # noqa: WPS432

    class Config:  # noqa: WPS431
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "etl_"
        fields = {
            "API_JWT": {
                "env": "API_JWT",
            },
        }


settings = Settings()
