import datetime as dt
import typing as t
import logging
import os
import sys

from pythonjsonlogger import jsonlogger


DEFAULT_LOGGER_NAME = "booktech"
LOGGER_ENV_DEV = "development"
LOGGER_ENV_PROD = "production"
LOGGER_ENV = (os.getenv("LOGGER_ENV", LOGGER_ENV_DEV)).lower()


class BooktechLogger:
    """A tiny wrapper class for logging to Gunicorn, STDOUT or a file.
    Example:
        .. code-block:: python

        log = BooktechLogger("Hello", logging.INFO)
        log.warning("Hello") # API call
    """

    def __init__(
        self,
        name: str = DEFAULT_LOGGER_NAME,
        env: str = LOGGER_ENV,
        level: int = logging.INFO,
        log_file: t.Optional[str] = None,
    ) -> None:
        """
        Args:
            name:
                Defaults to 'booktech'.
            level:
                The python logging level to set e.g. logging.ERROR,
                logging.WARNING etc.
        """
        self.name = name
        self.level = level
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)

        if env == LOGGER_ENV_PROD:

            # Create a gurnicorn logging handler
            handler, _ = self.get_gunicorn_handler()
            if handler is None:
                # App is not invoked by Gunicorn, get a stream logger
                handler = self.get_stream_handler(self.level, True)

            # Attach handlers to python root logger
            self.logger.addHandler(handler)
        else:
            # Get the log handler
            handler = (
                self.get_file_handler(log_file)
                if log_file is not None
                else self.get_stream_handler(level)
            )

            self.logger.addHandler(handler)

    def get_gunicorn_handler(self) -> t.Tuple[t.Optional[logging.Handler], int]:
        """Returns a logger which will add flask logs within gunicorn logs and
        also adhere to the logging level set by gunicorn"""

        # Set up logging via gunicorn
        gunicorn_logger = logging.getLogger("gunicorn.error")

        # Set gunicorn as log handler
        if gunicorn_logger.handlers:
            hdlr = gunicorn_logger.handlers[0]
            # Add json formatter
            formatter = CustomJsonFormatter(
                "%(timestamp)s %(level)s %(name)s %(message)s"
            )
            hdlr.setFormatter(formatter)
        else:
            hdlr = None

        # Let gunicorn set the logging level
        lvl = gunicorn_logger.level

        return hdlr, lvl

    def get_stream_handler(
        self, level: int, format_json: bool = False
    ) -> logging.StreamHandler:
        """Returns a stream logging handler"""

        # Create a stream stdout handler
        hdlr = logging.StreamHandler(sys.stdout)
        hdlr.setLevel(level)

        if format_json:
            # Add json formatter
            formatter = CustomJsonFormatter(
                "%(timestamp)s %(level)s %(name)s %(message)s"
            )
            hdlr.setFormatter(formatter)

        return hdlr

    def get_file_handler(self, log_file: str) -> logging.FileHandler:
        """Returns a file handler using the specified log_file."""

        # Create a file logger
        handler = logging.FileHandler(log_file)
        return handler

    def addHandler(self, hdlr) -> None:
        """Adds the specified handler hdlr to booktech logger."""
        if self.logger:
            self.logger.addHandler(hdlr)

    def setLevel(self, level: int) -> None:
        """
        Set the logging level of this logger. Level must be an int or a string.
        """
        self.logger.setLevel(level)
        self.level = self.logger.level

    def debug(self, msg, *args, **kwargs) -> None:
        """Log msgs with severity 'DEBUG'"""
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs) -> None:
        """Log msgs with severity 'INFO'"""
        self.logger.info(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs) -> None:
        """Log msgs with severity 'WARNING'"""
        self.logger.warning(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs) -> None:
        """Log msgs with severity 'WARNING'"""
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs) -> None:
        """Log msgs with severity 'ERROR'"""
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs) -> None:
        """Log msgs with severity 'CRITICAL'"""
        self.logger.critical(msg, *args, **kwargs)


def ProductionLogger(logger_name: str) -> BooktechLogger:
    """ProductionLogger attaches the gunicorn handler"""
    return BooktechLogger(logger_name, LOGGER_ENV_PROD)


def DevelopmentLogger(
    logger_name: str, log_file: t.Optional[str] = None
) -> BooktechLogger:
    """DevelopmentLogger attaches the stream or file handler"""
    return BooktechLogger(logger_name, LOGGER_ENV_DEV, log_file=log_file)


def GetLogger(
    logger_name: str,
    env: str = LOGGER_ENV_DEV,
    log_file: t.Optional[str] = None,
) -> BooktechLogger:
    """GetLogger returns a logger instance"""
    if env == LOGGER_ENV_PROD:
        return ProductionLogger(logger_name)
    return DevelopmentLogger(logger_name, log_file)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    A customized json formatter that adds timestamp, name and log level data
    """

    def add_fields(self, log_record, record, message_dict):
        """
        Hijacks the internal add_fields method and add extra meta data to a log
        records
        """
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

        if not log_record.get("timestamp"):
            # this doesn't use record.created, so it is slightly off
            now = dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now

        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


# Set up logging
log = GetLogger(DEFAULT_LOGGER_NAME, LOGGER_ENV)

