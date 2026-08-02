"""
Groq API key Manager.

Handles automatic failover between multiple
Groq API keys.
"""

from __future__ import annotations

from config.settings import GROQ_API_KEYS
from utils.logger import get_logger

logger = get_logger(__name__)

class GroqKeyManager:
    """
    Manages Groq API keys.
    
    Uses the primary key until it becomes
    unavailable (for example, due to a rate limit),
    then automatically switches to the next available key.
    """

    def __init__(self) -> None:

        if not GROQ_API_KEYS:
            raise ValueError(
                "No Groq API keys configured."
            )
        
        self._keys = GROQ_API_KEYS
        self._current_index = 0

    @property
    def current_key(self) -> str:
        """
        Return the currently activate API key.
        """
        return self._keys[
            self._current_index
        ]
    
    def switch_key(self) -> bool:
        """
        Switch to the next available API key.

        Returns:
            True if another key exists
            Flse if no backup keys ramain.
        """
        
        if self._current_index >= len(self._keys) -1:

            logger.warning(
                "No Backup Groq API keys avaiable"
            )

            return False
        
        self._current_index += 1

        logger.warning(
            "Switching to Groq API Key #%d",
            self._current_index + 1,
        )

        return True
    
    def reset(self) -> None:
        """
        Reset to primary API key.
        """

        self._current_index = 0

        logger.info(
            "Using primary Groq API key."
        )


groq_key_manager = GroqKeyManager()