"""
Utility functions for loaading prompt templates.
"""

from __future__ import annotations
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)

PROMPT_DIR = Path("prompts")


def load_prompt(
        filename: str,
) -> str:
    """
    Load a prompt template from the prompts directory.
    
    Args:
        filename:
            Prompt filename
            (e.g. "summarize.md)

    Returns:
        Prompt text.
    
    Raises:
        FileNotFoundError:
            If the prompt file does not exist.      
    """

    prompt_path = PROMPT_DIR / filename

    if not prompt_path.exists():

        logger.error(

            "Prompt file not found %s",
            prompt_path,
        )

        raise FileNotFoundError(
            f"Prompt file not found: {prompt_path}"
        )
    
    logger.info(
        "Loaded prompt file: %s",
        filename,
    )

    return prompt_path.read_text(
        encoding="utf-8"
    ).strip()
