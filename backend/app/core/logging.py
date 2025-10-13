import copy
import logging
import logging.config
from typing import Any

from app.types import LoggingLevelType


class RequestIDFilter(logging.Filter):
    """
    Logging filter that adds request_id to all log records.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        # Import here to avoid circular dependency
        from app.context import get_request_id

        # Add request_id to record, use "-" if not in request context
        record.request_id = get_request_id() or "-"
        return True


LOGGING_SIZE = 10 * 1024 * 1024
LOGGING_BACKUP_COUNT = 5

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {
            "()": "app.core.logging.RequestIDFilter",
        }
    },
    "formatters": {
        "generic": {
            "()": "logging.Formatter",
            "style": "{",
            "fmt": "{asctime}({levelname},{name})[{request_id}]: {message}",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
        }
    },
    "handlers": {
        "console": {
            "formatter": "generic",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": ["request_id"],
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "httpcore": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "authlib": {"handlers": ["console"], "level": "ERROR", "propagate": False},
    },
}


def configure_logging(level: LoggingLevelType = "INFO", config: dict[str, Any] | None = None) -> None:
    log_config = copy.deepcopy(LOGGING_CONFIG)

    if config:
        log_config.update(config)

    logging.config.dictConfig(log_config)

    logger = logging.getLogger("app")
    logger.setLevel(level)
