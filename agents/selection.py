"""
Selection Agent.

Selects the best articles for today's newsletter while
maintaining diversity across editorial source groups.
"""

from __future__ import annotations

from collections import defaultdict

from state.models import (
    Article,
    SourceGroup,
)

from state.news_state import NewsState

from config.settings import (
    NEWSLETTER_TOTAL_ARTICLES,
    SOURCE_GROUP_QUOTAS,
)

from utils.logger import get_logger

logger = get_logger(__name__)


class ArticleSelector:
    """
    Select the final articles for the newsletter.

    This agent applies source-group quotas and
    intelligently backfills remaining slots using the
    highest-ranked remaining articles.
    """

    def select_articles(
        self,
        articles: list[Article],
    ) -> list[Article]:
        """
        Select the final newsletter articles.

        Args:
            articles:
                Ranked articles.

        Returns:
            Selected articles.
        """

        logger.info(
            "Starting article selection..."
        )

        grouped_articles = self._group_articles(
            articles,
        )

        selected_articles = self._apply_quotas(
            grouped_articles,
        )

        selected_articles = self._backfill_articles(
            selected_articles,
            articles,
        )

        logger.info(
            "Selected %d articles for newsletter.",
            len(selected_articles),
        )

        return selected_articles

    def _group_articles(
        self,
        articles: list[Article],
    ) -> dict[SourceGroup, list[Article]]:
        """
        Group articles by editorial source group.

        Args:
            articles:
                Ranked articles.

        Returns:
            Dictionary mapping each SourceGroup
            to its corresponding articles.
        """

        grouped_articles: defaultdict[
            SourceGroup,
            list[Article],
        ] = defaultdict(list)

        for article in articles:

            grouped_articles[
                article.source.group
            ].append(article)

        logger.info(
            "Grouped %d articles into %d source groups.",
            len(articles),
            len(grouped_articles),
        )

        return dict(grouped_articles)


    def _apply_quotas(
        self,
        grouped_articles: dict[
            SourceGroup,
            list[Article],
        ],
    ) -> list[Article]:
        """
        Apply source-group quotas.

        Args:
            grouped_articles:
                Article grouped by SourceGroup.

        Returns:
            Articles selected according to configured quotas.
        """

        selected_articles: list[Article] = []

        for group, quota in SOURCE_GROUP_QUOTAS.items():

            articles = grouped_articles.get(
                group,
                [],
            )

            selected = articles[:quota]

            selected_articles.extend(selected)

            logger.info(
                "%s: selected %d/%d articles.",
                group.value,
                len(selected),
                quota,
            )
        
        logger.info(
            "Selected %d articles after applying quotas.",
            len(selected_articles),
        )

        return selected_articles



    def _backfill_articles(
        self,
        selected_articles: list[Article],
        ranked_articles: list[Article],
    ) -> list[Article]:
        """
        Fill remaining newsletter slots using the
        highest-ranked articles that have not yet
        been selected.

        Args:
            selected_articles:
                Articles selected afterapplying quotas.

            ranked_articles:
                All ranked articles.
        
        Returns:
            Final list of newsletter articles.
        """

        if len(selected_articles) >= NEWSLETTER_TOTAL_ARTICLES:

            selected_articles = selected_articles[:NEWSLETTER_TOTAL_ARTICLES]

            selected_articles.sort(
                key=lambda article: article.ranking_score,
                reverse=True,
            )
        


        selected_ids = {
            article.id
            for article in selected_articles
        }

        remaining_articles = [
            article
            for article in ranked_articles
            if article.id not in selected_ids
        ]

        remaining_slots = (
            NEWSLETTER_TOTAL_ARTICLES
            - len(selected_articles)
        )

        selected_articles.extend(
            remaining_articles[:remaining_slots]
        )

        logger.info(
            "Backfilled %d articles.",
            min(remaining_slots, len(remaining_articles)),
        )

        logger.info(
            "Final newsletter contains %d articles.",
            len(selected_articles),
        )

        return selected_articles



selector = ArticleSelector()


def selection_node(
    state: NewsState,
) -> NewsState:
    """
    LangGraph node responsible for selecting the
    final newsletter articles.
    """

    logger.info(
        "Starting Selection Agent..."
    )

    selected_articles = selector.select_articles(
        state["processed_articles"],
    )

    logger.info(
        "Selection Agent completed."
    )

    return {
        "processed_articles": selected_articles,
    }