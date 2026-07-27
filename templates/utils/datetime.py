"""
Utility functions for working with datetime values.
"""

from __future__ import annotations

import time
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


def parse_rss_datetime(
        published_parsed: time.struct_time | None,
) -> datetime:
    """
        Convert an RSS `published_parsed` value into a UTC datetime.

        Args:
            published_parsed:
                RSS publication time.

        Returns:
            Parsed UTC datetime. Falls back to the current UTC time if the
            publication date is unavailable.
    """

    if published_parsed:
        return datetime(
            *published_parsed[:6],
            tzinfo=UTC,
        )

    return datetime.now(UTC)