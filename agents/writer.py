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
            html_content: str,
    ) -> tuple[Path, Path]:
        """
        Save anewsletter
        
        Args:
            newsletter:
                Generated newsletter
            html_content:
                Generated HTML newsletter

        Returns:
            Tuple containing:
                (markdown_path, html_path)
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
        markdown_filename = (
            f"AI_Daily_News_"
            f"{newsletter.newsletter_date}.md"
        )

        markdown_path = (
            output_directory / markdown_filename
        )

        # --------------- Write markdown --------------- #
        markdown_path.write_text(
            newsletter.markdown_content or "",
            encoding="utf-8",
        )

        logger.info(
            "Newsletter saved to: %s",
            markdown_path,
        )

        # For the HTML

        html_filename = (
            f"AI_Daily_News_"
            f"{newsletter.newsletter_date}.html"
        )

        html_path = (
            output_directory / html_filename
        )

        html_path.write_text(
            html_content,
            encoding="utf-8",
        )

        logger.info(
            "HTML newsletter saved to: %s",
            html_path,
        )

        return (
            markdown_path, 
            html_path,
        )


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

    markdown_path, html_path = writer.save(
        state["newsletter"],
        state["html_content"]
    )

    logger.info(
        "Writer Agent Completed."
    )

    return{
        "output_path": str(markdown_path),
        "html_path": str(html_path),
    }