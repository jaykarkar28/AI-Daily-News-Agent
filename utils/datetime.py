"""
Utility functions for working with datetime values.
"""

from __future__ import annotations
from datetime import datetime, UTC

def parse_iso_datetime(value: str) -> datetime:
    """
    Convert an ISO-8601 datetime string into a timezone-aware datetime.

    Args:
        value: ISO datetime string.

    Returns:
        Parsed datetime.
    """

    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    ).astimezone(UTC)