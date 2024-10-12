import json
from typing import Any, Dict, List

from starlette.config import Config

config = Config()


class Settings:
    """Settings for the application"""

    PROJECT_NAME: str = config("PROJECT_NAME", cast=str, default="Insurance API")
    PROJECT_VERSION: str = config("PROJECT_VERSION", cast=str, default="1.0.0")

    RESOURCES_PATH: str = config("RESOURCES_PATH", cast=str, default="")
    LOG_LEVEL: str = config("LOG_LEVEL", cast=str, default="INFO").upper()
    LOG_FORMAT: str = config(
        "LOG_FORMAT",
        cast=str,
        default="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )

    LOGGER_NAME: str = config("LOGGER_NAME", cast=str, default="")

    # CORS Related configurations
    CORS_ALLOWED_ORIGINS: List[str] = json.loads(
        config("CORS_ALLOWED_ORIGINS", cast=str, default="[]")
    )
    CORS_ALLOWED_METHODS: List[str] = json.loads(
        config("CORS_ALLOWED_METHODS", cast=str, default='["*"]')
    )
    CORS_ALLOWED_HEADERS: List[str] = json.loads(
        config("CORS_ALLOWED_HEADERS", cast=str, default='["*"]')
    )

    # Database basic configuration
    INITIALIZE_DATABASE = config("INITIALIZE_DATABASE", cast=bool, default=True)
    HEALTHCHECK_DATABASE = config("HEALTHCHECK_DATABASE", cast=bool, default=False)

    # Cache settings
    CACHE_ENABLED = config("CACHE_ENABLED", cast=bool, default=True)
    CACHE_CONFIG: Dict[str, Any] = json.loads(
        config(
            "CACHE_CONFIG",
            cast=str,
            default=json.dumps(
                {
                    "default": {
                        "cache": "aiocache.RedisCache",
                        "endpoint": "127.0.0.1",
                        "port": 6379,
                        "db": 0,
                        "timeout": 5,
                        "serializer": {"class": "aiocache.serializers.JsonSerializer"},
                        "plugins": [
                            {"class": "aiocache.plugins.HitMissRatioPlugin"},
                            {"class": "aiocache.plugins.TimingPlugin"},
                        ],
                    },
                    "cache_redis_db1": {
                        "cache": "aiocache.RedisCache",
                        "endpoint": "127.0.0.1",
                        "port": 6379,
                        "db": 1,
                        "timeout": 5,
                        "serializer": {"class": "aiocache.serializers.JsonSerializer"},
                        "plugins": [
                            {"class": "aiocache.plugins.HitMissRatioPlugin"},
                            {"class": "aiocache.plugins.TimingPlugin"},
                        ],
                    },
                }
            ),
        )
    )

    OTEL_SERVICE_NAME: str = config(
        "OTEL_SERVICE_NAME", cast=str, default="my-fastapi-service"
    )
    OTEL_EXPORTER_OTLP_ENDPOINT: str = config(
        "OTEL_EXPORTER_OTLP_ENDPOINT", cast=str, default="http://otel-collector:4317"
    )


settings = Settings()
