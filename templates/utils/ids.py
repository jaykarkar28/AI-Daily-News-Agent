"""
Utility functions for generating unique and deterministic identifiers.
"""

from __future__ import annotations
import hashlib

def generate_article_id(url: str) -> str:
    """
    Generate a deterministic article ID from a URL.
    
    Args:
        url: Original article or repository URL.

    Returns:
        SHA-256 hexadecimal hash
    """

    return hashlib.sha256(
        url.encode("utf-8")
    ).hexdigest()