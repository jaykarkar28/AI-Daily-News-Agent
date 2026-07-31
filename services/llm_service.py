"""
Reusable LLM Service for the AI Daily News Agent.

This service provides a single interface for interacting with google's gemini models.
"""

from __future__ import annotations

import os 
import time

from google import genai
from google.genai import types
from typing import Any

from config.settings import (
    GEMINI_MODEL,
    GEMINI_TEMPERATURE,
    GEMINI_MAX_OUTPUT_TOKENS,
    GEMINI_MAX_RETRIES,
)

from utils.logger import get_logger

logger = get_logger(__name__)


from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

class LLMService:
    """
    Resuable wrapper around Google's Gemini API
    """

    def __init__(self) -> None:
        """
        Initialize the Gemini client.
        """

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables."
            )
        
        self.client = genai.Client(
            api_key=api_key,
        )

        logger.info(
            "Gemini client initialized successfully."
        )

    def generate_text(
            self,
            prompt: str,
    ) -> str | None :
        """
        Generate text using Gemini.

        Args:
            prompt: prompt sent to gemini.

        Returns:
            Generated text or None if generation fails.
        """

        for attempt in range(
            1,
            GEMINI_MAX_RETRIES + 1,
        ):
            
            try:

                response = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                    config = types.GenerateContentConfig(
                        temperature=GEMINI_TEMPERATURE,
                        max_output_tokens=GEMINI_MAX_OUTPUT_TOKENS,
                    ),
                )

                text = self._extract_response_text(response)

                logger.info(
                    "Gemini generation successful."
                )

                return text
        
            except Exception as exc:

                logger.warning(
                    "Gemini Request failed "
                    "(attempt %d/%d): %s",
                    attempt,
                    GEMINI_MAX_RETRIES,
                    exc,
                )

                time.sleep(attempt)

        logger.error(
            "Gemini request failed after %d attempts.",
            GEMINI_MAX_RETRIES,
        )

        return None
    

    def _extract_response_text(
            self,
            response: Any,
    ) -> str:
        """
        Extract text from Gemini response.
        """

        if(
            response is None
            or response.text is None
        ):
            return ""
        
        return response.text.strip()
    


llm_service = LLMService()

