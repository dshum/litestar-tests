from logging import getLevelName, INFO

from litestar.logging import LoggingConfig

logging_config = LoggingConfig(
    root={"level": getLevelName(INFO), "handlers": ["console"]},
    formatters={
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
    },
)
