"""
Global article deduplication node.
"""

from __future__ import annotations

from utils.logger import get_logger
from state.models import Article  
from state.news_state import NewsState
from typing import Any

logger = get_logger(__name__)

class ArticleDeduplicator:
    """
    Removes duplicate articles collected from different sources.
    """

    def deduplicate(
            self,
            articles: list[Article],
    ) -> list[Article]:
        
        """
        Remove duplicate articles from the collected article list.
        """

        logger.info(
            "Deduplicating %d collected articles",
            len(articles),
        )

        unique_articles = self._remove_duplicate_urls(
            articles
        )

        duplicates_removed = len(articles) - len(unique_articles)

        logger.info(
            "Deduplicated %d articles into %d unique articles (%d duplicates removed).",
            len(articles),
            len(unique_articles),
            duplicates_removed,
        )

        return unique_articles


    def _remove_duplicate_urls(self,
            articles: list[Article],
    ) -> list[Article]:
        """
        Remove duplicate articles based on their URL
        """

        articles_by_url: dict[str, Article] = {}

        for article in articles:
            articles_by_url[article.url] = article

        return list(articles_by_url.values())



def deduplicator_node(
        state: dict[str, Any]
)-> dict[str, Any]:
    """
    Global article duplication node.
    """

    logger.info("Deduplicator node started.")

    deduplicator = ArticleDeduplicator()

    unique_articles = deduplicator.deduplicate(
        state["articles"],
    )

    state[
        "execution_info"
    ].total_articles = len(
        unique_articles
    )


    return {
        **state,
        "processed_articles": unique_articles,
    }