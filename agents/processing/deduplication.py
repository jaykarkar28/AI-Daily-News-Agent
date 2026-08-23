"""
Global article deduplication.

Removes duplicate news articles collected from
multiple sources while prioritizing higher-quality
and more trusted sources.
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from state.models import Article
from state.news_state import NewsState
from utils.logger import get_logger


logger = get_logger(__name__)


class GlobalDeduplicator:
    """
    Remove duplicate articles from the complete
    news collection.

    Duplicate detection is performed using:

    1. Normalized URLs
    2. Normalized article titles

    When duplicates are found, the article with the
    highest quality score is kept.
    """

    def deduplicate(
        self,
        articles: list[Article],
    ) -> list[Article]:
        """
        Remove duplicate articles globally.

        Args:
            articles:
                Articles collected from all sources.

        Returns:
            A deduplicated list of articles.
        """

        logger.info(
            "Starting global deduplication for %d articles.",
            len(articles),
        )

        if not articles:
            return []

        # First pass: exact URL duplicates.
        url_deduplicated = self._deduplicate_by_url(
            articles,
        )

        # Second pass: duplicate titles.
        title_deduplicated = self._deduplicate_by_title(
            url_deduplicated,
        )

        # Sort newest articles first.
        title_deduplicated.sort(
            key=lambda article: article.published_at,
            reverse=True,
        )

        removed_count = (
            len(articles)
            - len(title_deduplicated)
        )

        logger.info(
            "Global deduplication completed: %d -> %d articles. "
            "Removed %d duplicates.",
            len(articles),
            len(title_deduplicated),
            removed_count,
        )

        return title_deduplicated

    # --------------------------------------------------
    # URL Deduplication
    # --------------------------------------------------

    def _deduplicate_by_url(
        self,
        articles: list[Article],
    ) -> list[Article]:
        """
        Remove articles with duplicate normalized URLs.
        """

        grouped_articles: dict[
            str,
            list[Article],
        ] = defaultdict(list)

        for article in articles:

            normalized_url = self._normalize_url(
                article.url,
            )

            grouped_articles[
                normalized_url
            ].append(article)

        unique_articles: list[Article] = []

        for duplicate_group in grouped_articles.values():

            best_article = self._select_best_article(
                duplicate_group,
            )

            unique_articles.append(
                best_article,
            )

        logger.info(
            "URL deduplication: %d -> %d articles.",
            len(articles),
            len(unique_articles),
        )

        return unique_articles

    # --------------------------------------------------
    # Title Deduplication
    # --------------------------------------------------

    def _deduplicate_by_title(
        self,
        articles: list[Article],
    ) -> list[Article]:
        """
        Remove articles with identical normalized titles.
        """

        grouped_articles: dict[
            str,
            list[Article],
        ] = defaultdict(list)

        for article in articles:

            normalized_title = self._normalize_title(
                article.title,
            )

            grouped_articles[
                normalized_title
            ].append(article)

        unique_articles: list[Article] = []

        for duplicate_group in grouped_articles.values():

            best_article = self._select_best_article(
                duplicate_group,
            )

            unique_articles.append(
                best_article,
            )

        logger.info(
            "Title deduplication: %d -> %d articles.",
            len(articles),
            len(unique_articles),
        )

        return unique_articles

    # --------------------------------------------------
    # Best Article Selection
    # --------------------------------------------------

    def _select_best_article(
        self,
        articles: list[Article],
    ) -> Article:
        """
        Select the best article from a duplicate group.

        Priority:
        1. Higher trust score
        2. Official source
        3. Newer publication date
        """

        return max(
            articles,
            key=self._article_quality_score,
        )

    def _article_quality_score(
        self,
        article: Article,
    ) -> tuple[float, int, Any]:
        """
        Create a comparable quality score for an article.
        """

        return (
            article.trust_score,
            int(article.source.is_official),
            article.published_at,
        )

    # --------------------------------------------------
    # URL Normalization
    # --------------------------------------------------

    def _normalize_url(
        self,
        url: str,
    ) -> str:
        """
        Normalize URLs before duplicate comparison.
        """

        normalized = url.lower().strip()

        # Remove protocol.
        normalized = re.sub(
            r"^https?://",
            "",
            normalized,
        )

        # Remove www.
        normalized = re.sub(
            r"^www\.",
            "",
            normalized,
        )

        # Remove query parameters and fragments.
        normalized = normalized.split(
            "?",
            1,
        )[0]

        normalized = normalized.split(
            "#",
            1,
        )[0]

        # Remove trailing slash.
        normalized = normalized.rstrip(
            "/",
        )

        return normalized

    # --------------------------------------------------
    # Title Normalization
    # --------------------------------------------------

    def _normalize_title(
        self,
        title: str,
    ) -> str:
        """
        Normalize article titles before comparison.
        """

        normalized = title.lower().strip()

        # Remove punctuation.
        normalized = re.sub(
            r"[^\w\s]",
            " ",
            normalized,
        )

        # Normalize multiple spaces.
        normalized = re.sub(
            r"\s+",
            " ",
            normalized,
        )

        return normalized.strip()


# --------------------------------------------------
# LangGraph Node
# --------------------------------------------------

def global_deduplication_node(
    state: NewsState,
) -> dict[str, Any]:
    """
    LangGraph node that performs global article
    deduplication.
    """

    articles = state.get(
        "articles",
        [],
    )

    logger.info(
        "Global Deduplication node received %d articles.",
        len(articles),
    )

    deduplicator = GlobalDeduplicator()

    deduplicated_articles = deduplicator.deduplicate(
        articles,
    )

    logger.info(
        "Global Deduplication node returning %d articles.",
        len(deduplicated_articles),
    )

    return {
        "articles": deduplicated_articles,
    }