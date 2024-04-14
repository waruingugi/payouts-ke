import logging
import os.path
import sys
from functools import lru_cache
from typing import cast


class SourceFormatter(logging.Formatter):
    def format(self, record):
        """Customize logger so that it always prepends the source file/module of the log"""
        module, func = record.module, record.funcName

        path_parts = record.pathname.split(os.sep)
        module, file_name = path_parts[-2], path_parts[-1]

        # Prepend information to the log message
        record.msg = f"{module}:{file_name}:{func}: {record.msg}"

        # Call the original formatter to apply any additional formatting
        return super(SourceFormatter, self).format(record)


@lru_cache
def instantiate_logger() -> logging.Logger:
    logger_ = logging.getLogger(__name__)
    logger_.setLevel(logging.INFO)

    # Set the source formatter
    formatter = SourceFormatter("[%(asctime)s] %(levelname)s - %(message)s")

    # Create a stream handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger_.addHandler(handler)

    return logger_


logger = cast(logging.Logger, instantiate_logger())
