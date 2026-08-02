"""
Github Quality Filter.

Filters GitHub repositories to keep only 
repositories that are genuinely AI-related.
"""

from __future__ import annotations

from config.settings import (
    GITHUB_AI_KEYWORDS,
    GITHUB_BLACKLIST_KEYWORDS,
    GITHUB_MIN_AI_SCORE,
    GITHUB_TRUSTED_OWNERS,
)

from state.models import (
    Article,
    SourceType,
)

from datetime import datetime, UTC, timedelta

from state.news_state import NewsState
from utils.logger import get_logger

logger = get_logger(__name__)   


class GitHubFilter:
    """
    Filters GitHub repositories based on
    AI relevance
    """

    def filter_articles(
            self,
            articles: list[Article],
    ) -> list[Article]:
        """
        Filter Github repositories while leaving
        all non-GitHub articles untouched.
        """ 

        filtered_articles: list[Article] = []

        accepted = 0
        rejected = 0

        logger.info(
            "Starting GitHub Quality Filter..."
        )

        for article in articles:

            # RSS /  Official articles always pass
            if article.source.source_type != SourceType.GITHUB:

                filtered_articles.append(article)
                continue

            score = self._calcuate_score(article)

            if score >= GITHUB_MIN_AI_SCORE:

                accepted += 1
                filtered_articles.append(article)

                logger.info(
                    "Accepted (%d): %s",
                    score,
                    article.title,
                )
            
            else:
                rejected += 1

        logger.info(
            "Github Filtered completed."
        )

        logger.info(
            "Accepted: %d",
            accepted,
        )

        logger.info(
            "Rejected: %d",
            rejected,
        )

        return filtered_articles
    
    def _calcuate_score(
            self,
            article: Article,
    ) -> int:
        """
        Calculate AI relevance score of a Github repository.

        Higher score = more likely to be a genuine AI repository
        """

        score = 0

        title = (article.title or "").lower()
        summary = (article.summary or "").lower()

        tags = [
            tag.lower()
            for tag in article.tags
        ]

        source_name = (
            article.source.name or ""
        ).lower()


        # ---------- Repository name ----------

        for keyword in GITHUB_AI_KEYWORDS:

            if keyword in title:
                score += 4

        # ---------- Repository description ----------

        for keyword in GITHUB_AI_KEYWORDS:

            if keyword in summary:
                score += 3

        # ---------- GitHub Topics ----------

        for tag in tags:

            if tag in GITHUB_AI_KEYWORDS:
                score += 3

        # ---------- Trusted Owners ----------

        for owner in GITHUB_TRUSTED_OWNERS:

            if owner in source_name:
                score += 4

        # ---------- Blacklist Keywords ----------

        for keyword in GITHUB_BLACKLIST_KEYWORDS:

            if (
                keyword in title 
                or keyword in summary
            ):
                score -= 6

        # --------- Recently Updated ----------

        if article.published_at >= (
            datetime.now(UTC) - timedelta(days=30)
        ):
            score += 2
        
        return score

        

github_filter = GitHubFilter()

def github_filter_node(
        state: NewsState,
) -> NewsState:
    """
    Langgraph node
    """

    filtered_articles = github_filter.filter_articles(
        state["processed_articles"],
    )

    return {
        "processed_articles": filtered_articles,
    }

    