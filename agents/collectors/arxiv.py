"""
arXiv Research Collector.

Collects the latest AI/ML research papers from arXiv
and converts them into the project's standard Article model.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from agents.collectors.base import BaseCollector

from config.settings import (
    ARXIV_MAX_AGE_DAYS,
    ARXIV_HIGH_PRIORITY_KEYWORDS,
    ARXIV_HIGH_PRIORITY_SCORE,
    ARXIV_LOW_PRIORITY_KEYWORDS,
    ARXIV_LOW_PRIORITY_SCORE,
    ARXIV_MAX_ARTICLES,
    ARXIV_MEDIUM_PRIORITY_KEYWORDS,
    ARXIV_MEDIUM_PRIORITY_SCORE,
    ARXIV_MIN_RELEVANCE_SCORE,
    ARXIV_TRUST_SCORE,
    ARXIV_DOMAIN_PENALTY_KEYWORDS,
    ARXIV_DOMAIN_PENALTY_SCORE,
)

from services.llm_service import llm_service
from state.models import (
    Article,
    Source,
    SourceGroup,
    SourceType,
)
from state.news_state import NewsState

from tools.arxiv_api import arxiv_api
from utils.ids import generate_article_id
from utils.logger import get_logger


logger = get_logger(__name__)


class ArxivCollector(BaseCollector):
    """
    Collect and process the latest AI/ML research
    papers from arXiv.
    """
    
    def _calculate_relevance_score(
        self,
        article: Article,
    ) -> int:
        """
        Calculate the AI relevance score for an article.

        The final score considers:

        - High-priority AI topics
        - Medium-priority AI topics
        - Low-priority AI/ML topics
        - Domain-specific relevance penalties
        """

        text = (
            f"{article.title} "
            f"{article.summary or ''}"
        ).lower()

        high_matches = sum(
            keyword.lower() in text
            for keyword in ARXIV_HIGH_PRIORITY_KEYWORDS
        )

        medium_matches = sum(
            keyword.lower() in text
            for keyword in ARXIV_MEDIUM_PRIORITY_KEYWORDS
        )

        low_matches = sum(
            keyword.lower() in text
            for keyword in ARXIV_LOW_PRIORITY_KEYWORDS
        )

        domain_matches = sum(
            keyword.lower() in text
            for keyword in ARXIV_DOMAIN_PENALTY_KEYWORDS
        )

        score = (
            high_matches
            * ARXIV_HIGH_PRIORITY_SCORE
        )

        score += (
            medium_matches
            * ARXIV_MEDIUM_PRIORITY_SCORE
        )

        score += (
            low_matches
            * ARXIV_LOW_PRIORITY_SCORE
        )

        score -= (
            domain_matches
            * ARXIV_DOMAIN_PENALTY_SCORE
        )

        return max(score, 0)


    def _filter_ai_relevant_articles(
        self,
        articles: list[Article],
    ) -> list[Article]:
        """
        Keep only sufficiently relevant AI/ML papers.

        Each paper receives a relevance score based on
        configured keyword priorities.
        """

        scored_articles: list[
            tuple[Article, int]
        ] = []

        for article in articles:

            score = self._calculate_relevance_score(
                article,
            )

            if score >= ARXIV_MIN_RELEVANCE_SCORE:

                scored_articles.append(
                    (
                        article,
                        score,
                    )
                )

        scored_articles.sort(
            key=lambda item: (
                item[1],
                item[0].published_at,
            ),
            reverse=True,
        )

        relevant_articles = [
            article
            for article, score in scored_articles
        ]

        logger.info(
            "Kept %d/%d AI-relevant arXiv papers "
            "with minimum relevance score %d.",
            len(relevant_articles),
            len(articles),
            ARXIV_MIN_RELEVANCE_SCORE,
        )

        return relevant_articles

    def collect(self) -> list[Article]:
        """
        Collect recent research papers from arXiv.

        Returns:
            List of valid and recent Article objects.
        """

        logger.info(
            "Starting arXiv research paper collection."
        )

        raw_results = arxiv_api.search_latest_papers() or []

        articles = self._convert_results_to_articles(
            raw_results,
        )

        recent_articles = self._filter_recent_articles(
            articles,
        )
        
        relevant_articles = self._filter_ai_relevant_articles(
            recent_articles,
        )

        logger.info(
            "Collected %d AI/ML - relevant arxiv research papers.",
            len(relevant_articles),
        )

        return relevant_articles

    def _convert_results_to_articles(
        self,
        raw_results: list[Any],
    ) -> list[Article]:
        """
        Convert raw arXiv results into Article objects.

        Args:
            raw_results:
                Raw arXiv Result objects.

        Returns:
            List of converted Article objects.
        """

        articles: list[Article] = []

        source = Source(
            name="arXiv",
            url="https://arxiv.org",
            source_type=SourceType.ARXIV,
            group=SourceGroup.RESEARCH,
            is_official=False,
            trust_score=ARXIV_TRUST_SCORE,
        )

        for result in raw_results:

            try:
                paper = arxiv_api.result_to_dict(
                    result,
                )

                article = Article(
                    id=generate_article_id(
                        paper["url"],
                    ),
                    title=paper["title"],
                    url=paper["url"],
                    source=source,
                    published_at=paper["published_at"],
                    summary=paper["summary"],
                    trust_score=ARXIV_TRUST_SCORE,
                )

                articles.append(article)

            except Exception:
                logger.exception(
                    "Failed to convert arXiv paper: %s",
                    getattr(
                        result,
                        "title",
                        "Unknown",
                    ),
                )

        logger.info(
            "Converted %d arXiv results into Article objects.",
            len(articles),
        )

        return articles

    def _filter_recent_articles(
        self,
        articles: list[Article],
    ) -> list[Article]:
        """
        Keep only recently published research papers.

        Papers are sorted from newest to oldest and
        limited to the configured maximum.

        Args:
            articles:
                Converted arXiv articles.

        Returns:
            Recent research articles.
        """

        cutoff_date = datetime.now(
            UTC,
        ) - timedelta(
            days=ARXIV_MAX_AGE_DAYS,
        )

        recent_articles = [
            article
            for article in articles
            if article.published_at >= cutoff_date
        ]

        recent_articles.sort(
            key=lambda article: article.published_at,
            reverse=True,
        )

        return recent_articles[
            :ARXIV_MAX_ARTICLES
        ]


def arxiv_collector_node(
    state: NewsState,
) -> dict[str, Any]:
    """
    LangGraph node responsible for collecting
    the latest arXiv research papers.
    """

    logger.info(
        "Starting arXiv Collector..."
    )

    collector = ArxivCollector()

    articles = collector.collect()

    logger.info(
        "arXiv Collector completed with %d articles.",
        len(articles),
    )

    return {
        "articles": articles,
    }