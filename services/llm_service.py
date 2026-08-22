# """
# Reusable LLM Service for the AI Daily News Agent.

# This service provides a single interface for interacting
# with Groq LLMs.
# """

# from __future__ import annotations

# import os
# import time
# from typing import Any

# from dotenv import load_dotenv
# from groq import Groq

# from config.settings import (
#     GROQ_MODEL,
#     GROQ_TEMPERATURE,
#     GROQ_MAX_OUTPUT_TOKENS,
#     GROQ_MAX_RETRIES,
# )

# from utils.logger import get_logger

# load_dotenv()

# logger = get_logger(__name__)


# class LLMService:
#     """
#     Reusable wrapper around the Groq API.
#     """

#     def __init__(self) -> None:
#         """
#         Initialize the LLM service.

#         The Groq client is created lazily on the
#         first request instead of during application startup.
#         """

#         self.client: Groq | None = None

#     def _initialize_client(self) -> None:
#         """
#         Initialize the Groq client if it has not
#         already been created.
#         """

#         if self.client is not None:
#             return

#         api_key = os.getenv("GROQ_API_KEY")

#         if not api_key:
#             raise ValueError(
#                 "GROQ_API_KEY not found in environment variables."
#             )

#         self.client = Groq(
#             api_key=api_key,
#         )

#         logger.info(
#             "Groq client initialized successfully."
#         )

#     def generate_text(
#         self,
#         prompt: str,
#     ) -> str | None:
#         """
#         Generate text using Groq.

#         Args:
#             prompt:
#                 Prompt sent to the LLM.

#         Returns:
#             Generated text if successful,
#             otherwise None.
#         """

#         self._initialize_client()

#         for attempt in range(
#             1,
#             GROQ_MAX_RETRIES + 1,
#         ):

#             try:

#                 response = self.client.chat.completions.create(
#                     model=GROQ_MODEL,
#                     messages=[
#                         {
#                             "role": "user",
#                             "content": prompt,
#                         }
#                     ],
#                     temperature=GROQ_TEMPERATURE,
#                     max_completion_tokens=GROQ_MAX_OUTPUT_TOKENS,
#                 )

#                 text = self._extract_response_text(
#                     response,
#                 )

#                 logger.info(
#                     "Text generation successful."
#                 )

#                 return text

#             except Exception as exc:

#                 logger.warning(
#                     "LLM request failed "
#                     "(attempt %d/%d): %s",
#                     attempt,
#                     GROQ_MAX_RETRIES,
#                     exc,
#                 )

#                 time.sleep(
#                     2 ** (attempt - 1)
#                 )

#         logger.error(
#             "LLM request failed after %d attempts.",
#             GROQ_MAX_RETRIES,
#         )

#         return None

#     def _extract_response_text(
#         self,
#         response: Any,
#     ) -> str:
#         """
#         Extract generated text from a Groq response.

#         Args:
#             response:
#                 Groq response object.

#         Returns:
#             Generated text.
#         """

#         if (
#             response is None
#             or not response.choices
#         ):
#             return ""

#         message = response.choices[0].message

#         if (
#             message is None
#             or message.content is None
#         ):
#             return ""

#         return message.content.strip()


# llm_service = LLMService()






"""
Reusable LLM Service for the AI Daily News Agent.

This service provides a single interface for interacting
with Groq LLMs and supports API key rotation.
"""

from __future__ import annotations

import time
from typing import Any

from groq import Groq

from config.settings import (
    GROQ_API_KEYS,
    GROQ_MAX_OUTPUT_TOKENS,
    GROQ_MAX_RETRIES,
    GROQ_MODEL,
    GROQ_TEMPERATURE,
)

from utils.logger import get_logger


logger = get_logger(__name__)


class LLMService:
    """
    Reusable wrapper around the Groq API.

    Supports multiple Groq API keys and automatically
    rotates to another key when a request fails.
    """

    def __init__(self) -> None:
        """
        Initialize the LLM service.
        """

        if not GROQ_API_KEYS:
            raise ValueError(
                "No Groq API keys found. "
                "Please configure GROQ_API_KEY_PRIMARY "
                "or GROQ_API_KEY_BACKUP."
            )

        self.api_keys = GROQ_API_KEYS
        self.current_key_index = 0
        self.client: Groq | None = None

        logger.info(
            "LLM Service initialized with %d Groq API key(s).",
            len(self.api_keys),
        )

    def _initialize_client(self) -> None:
        """
        Initialize the Groq client using the current API key.
        
        Internal SDK retries are disabled so that rate-limit
        errors can be handled by our own API key rotation logic.
        """
        
        api_key = self.api_keys[self.current_key_index]
        
        self.client = Groq(
            api_key=api_key,
            max_retries=0  # Disable internal SDK retries
        )
        
        logger.info(
            "Groq client initialized using API key %d/%d",
            self.current_key_index + 1,
            len(self.api_keys)
        )

        

    def _rotate_api_key(self) -> bool:
        """
        Switch to the next available Groq API key.

        Returns:
            True if another API key is available,
            otherwise False.
        """
        
        if len(self.api_keys) <= 1:
            return False  # No other keys to rotate to
        
        previous_key_index = self.current_key_index
        
        self.current_key_index = (
            self.current_key_index + 1
        ) % len(self.api_keys)
        
        # Force creation of a new client using
        # the newly selected API key.
        
        self.client = None
        
        logger.warning(
            "Groq API key rotated: %d/%d -> %d/%d.",
            previous_key_index + 1,
            len(self.api_keys),
            self.current_key_index + 1,
            len(self.api_keys),
        )
        
        return True

    def _is_rate_limit_error(
        self,
        exception: Exception,
    ) -> bool:
        """
        Check whether an exception is caused by
        a Groq API rate limit.
        """

        error_message = str(
            exception
        ).lower()

        return (
            "429" in error_message
            or "rate limit" in error_message
            or "too many requests" in error_message
        )

    def generate_text(
        self,
        prompt: str,
    ) -> str | None:
        """
        Generate text using Groq.

        Automatically retries requests and rotates
        between configured API keys when necessary.

        Args:
            prompt:
                Prompt sent to the LLM.

        Returns:
            Generated text if successful,
            otherwise None.
        """

        total_keys = len(
            self.api_keys
        )

        for key_attempt in range(
            total_keys
        ):

            self._initialize_client()

            for attempt in range(
                1,
                GROQ_MAX_RETRIES + 1,
            ):

                try:

                    response = (
                        self.client.chat.completions.create(
                            model=GROQ_MODEL,
                            messages=[
                                {
                                    "role": "user",
                                    "content": prompt,
                                }
                            ],
                            temperature=GROQ_TEMPERATURE,
                            max_completion_tokens=(
                                GROQ_MAX_OUTPUT_TOKENS
                            ),
                        )
                    )

                    text = self._extract_response_text(
                        response,
                    )

                    logger.info(
                        "Text generation successful "
                        "using Groq API key %d/%d.",
                        self.current_key_index + 1,
                        total_keys,
                    )

                    return text

                except Exception as exc:

                    if self._is_rate_limit_error(
                        exc
                    ):

                        logger.warning(
                            "Groq rate limit detected "
                            "on API key %d/%d.",
                            self.current_key_index + 1,
                            total_keys,
                        )

                        break

                    logger.warning(
                        "LLM request failed using "
                        "API key %d/%d "
                        "(attempt %d/%d): %s",
                        self.current_key_index + 1,
                        total_keys,
                        attempt,
                        GROQ_MAX_RETRIES,
                        exc,
                    )

                    if attempt < GROQ_MAX_RETRIES:

                        delay = 2 ** (
                            attempt - 1
                        )

                        logger.info(
                            "Retrying after %d second(s).",
                            delay,
                        )

                        time.sleep(
                            delay
                        )

            if key_attempt < total_keys - 1:

                self._rotate_api_key()

        logger.error(
            "LLM request failed after trying "
            "%d Groq API key(s).",
            total_keys,
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

        message = response.choices[
            0
        ].message

        if (
            message is None
            or message.content is None
        ):
            return ""

        return message.content.strip()


llm_service = LLMService()        
                
                        
                        
                    
        
        
        
        
        
        
    
    


