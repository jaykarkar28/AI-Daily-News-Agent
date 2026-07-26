"""
Application-wide logging configuration.
"""

from __future__ import annotations

import logging
from pathlib import Path


# Indicates whether logging has already been configured.

def setup_logging() -> None:
    """
    Configure application-wide logging.

    This should be called once when the application starts.
    Logs are written to both the console and logs/app.log.
    """    

    root_logger = logging.getLogger("")

    if root_logger.hasHandlers():
        # Logging is already configured, so we don't need to do it again.
        return
    
    # Create the logs directory if it doesn't exist

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "app.log"

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Write logs to file.
    file_handler = logging.FileHandler(
        log_file,
        mode="w",
        encoding="utf-8",
        )
    file_handler.setFormatter(formatter)

    # Show logs in terminal.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)


    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger.
    
    Args:
        name: Usually __name__ of the caller.

    Returns:
        Configured Logger instance.
    """

    return logging.getLogger(name)