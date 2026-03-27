import logging
import sys
from typing import Optional

from loguru import logger

from src.core.config import CONFIG


class LoguruInterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


def disable_mongo_debug_logs():
    mongo_logger = logging.getLogger("pymongo")
    mongo_logger.setLevel(logging.INFO)


def configure_logger(
    capture_exceptions: bool = False, subfolder: Optional[str] = None
) -> None:
    logger.remove()

    level = "DEBUG" if CONFIG.debug else "INFO"
    logging_level = logging.DEBUG if CONFIG.debug else logging.INFO

    log_format = "log_{time:YYYY-MM-DD}.log"
    subdirectory = "logs" if not subfolder else f"logs/{subfolder}"

    logger.add(
        f"{subdirectory}/{log_format}",
        rotation="12:00",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}",
        level="INFO",
        encoding="utf-8",
        compression="zip",
        colorize=True,
    )
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | "
        + "<level>{level}</level> | {file}:{line} | "
        "{message}",
        level=level,
    )
    if capture_exceptions:
        logger.add(
            f"{subdirectory}/errors/error_{log_format}",
            rotation="12:00",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}",
            level="ERROR",
            encoding="utf-8",
            compression="zip",
        )

    logging.basicConfig(handlers=[LoguruInterceptHandler()], level=logging_level)
    disable_mongo_debug_logs()
