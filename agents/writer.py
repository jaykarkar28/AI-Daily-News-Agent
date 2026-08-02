"""
Writer Agent.
Saves the generated newsletter to disk.
"""

from __future__ import annotations

from pathlib import Path

from state.models import Newsletter
from state.news_state import NewsState

from utils.logger import get_logger


logger = get_logger(__name__)

class NewsletterWriter:
    """
    Save newsletter to disk.
    """

    def save(
            self,
            newsletter: Newsletter,
    ) -> Path:
        """
        Save anewsletter
        
        Args:
            newsletter:
                Generated newsletter

        Returns:
            Path of the saved file.
        """

        # --------------- Create Output Directory --------------- #
        output_directory = Path(
            "newsletters"
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        # --------------- Build filename --------------- #
        filename = (
            f"AI_Daily_News_"
            f"{newsletter.newsletter_date}.md"
        )

        output_path = (
            output_directory / filename
        )

        # --------------- Write markdown --------------- #
        output_path.write_text(
            newsletter.markdown_content or "",
            encoding="utf-8",
        )

        logger.info(
            "Newsletter saved to: %s",
            output_path,
        )

        return output_path


writer = NewsletterWriter()



def writer_node(
        state: NewsState,
) -> NewsState:
    """
    LangGraph node responsible for
    saving the nresletter.
    """

    logger.info(
        "Starting Writer Agent..."
    )

    output_path = writer.save(
        state["newsletter"]
    )

    logger.info(
        "Writer Agent Completed."
    )

    return{
        "output_path": str(output_path),
    }