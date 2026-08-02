"""
Reusable LLM Service for the AI Daily News Agent.

This service provides a single interface for interacting
with Groq LLMs.
"""

from __future__ import annotations

import os
import time
from typing import Any

from dotenv import load_dotenv
from groq import Groq

from config.settings import (
    GROQ_MODEL,
    GROQ_TEMPERATURE,
    GROQ_MAX_OUTPUT_TOKENS,
    GROQ_MAX_RETRIES,
)

from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class LLMService:
    """
    Reusable wrapper around the Groq API.
    """

    def __init__(self) -> None:
        """
        Initialize the LLM service.

        The Groq client is created lazily on the
        first request instead of during application startup.
        """

        self.client: Groq | None = None

    def _initialize_client(self) -> None:
        """
        Initialize the Groq client if it has not
        already been created.
        """

        if self.client is not None:
            return

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in environment variables."
            )

        self.client = Groq(
            api_key=api_key,
        )

        logger.info(
            "Groq client initialized successfully."
        )

    def generate_text(
        self,
        prompt: str,
    ) -> str | None:
        """
        Generate text using Groq.

        Args:
            prompt:
                Prompt sent to the LLM.

        Returns:
            Generated text if successful,
            otherwise None.
        """

        self._initialize_client()

        for attempt in range(
            1,
            GROQ_MAX_RETRIES + 1,
        ):

            try:

                response = self.client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    temperature=GROQ_TEMPERATURE,
                    max_completion_tokens=GROQ_MAX_OUTPUT_TOKENS,
                )

                text = self._extract_response_text(
                    response,
                )

                logger.info(
                    "Text generation successful."
                )

                return text

            except Exception as exc:

                logger.warning(
                    "LLM request failed "
                    "(attempt %d/%d): %s",
                    attempt,
                    GROQ_MAX_RETRIES,
                    exc,
                )

                time.sleep(
                    2 ** (attempt - 1)
                )

        logger.error(
            "LLM request failed after %d attempts.",
            GROQ_MAX_RETRIES,
        )

        return None

    def _extract_response_text(
        self,
        response: Any,
    ) -> str:
        """
        Extract generated text from a Groq response.

        Args:
            response:
                Groq response object.

        Returns:
            Generated text.
        """

        if (
            response is None
            or not response.choices
        ):
            return ""

        message = response.choices[0].message

        if (
            message is None
            or message.content is None
        ):
            return ""

        return message.content.strip()


llm_service = LLMService()