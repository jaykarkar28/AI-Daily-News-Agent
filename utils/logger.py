"""
Application-wide logging configuration.
"""

from __future__ import annotations
import logging

def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger.
    
    Args:
        name: Usually __name__ of the caller.

    Returns:
        Configured Logger instance.
    """

    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    return logging.getLogger(name)