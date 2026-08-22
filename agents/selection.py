"""
Selection Agent.

Selects the best articles for today's newsletter while
maintaining diversity across editorial source groups
and individual RSS sources.
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
    RSS_SOURCE_QUOTAS,
)

from utils.logger import get_logger


logger = get_logger(__name__)


class ArticleSelector:
    """
    Select the final articles for the newsletter.

    This agent applies:

    1. Editorial source-group quotas.
    2. Individual RSS source quotas.
    3. Intelligent backfilling using ranked articles.

    This prevents one RSS source, such as OpenAI,
    from dominating the final newsletter.
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
    ) -> dict[
        SourceGroup,
        list[Article],
    ]:
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
        Apply source-group and individual-source quotas.

        The selection process works in two levels:

        1. SourceGroup quota:
           Controls how many articles can come from
           Official, Research, Open Source, etc.

        2. RSS source quota:
           Controls how many articles can initially
           be selected from an individual source such
           as OpenAI, Anthropic, or Google DeepMind.

        Any unused group slots are then filled using
        the highest-ranked remaining articles from
        that same source group.

        Args:
            grouped_articles:
                Articles grouped by SourceGroup.

        Returns:
            Articles selected according to configured
            quotas.
        """

        selected_articles: list[Article] = []

        for group, group_quota in SOURCE_GROUP_QUOTAS.items():

            articles = grouped_articles.get(
                group,
                [],
            )

            if not articles:

                logger.info(
                    "%s: no articles available.",
                    group.value,
                )

                continue

            # --------------------------------------------------
            # Group articles by individual source.
            # --------------------------------------------------

            source_articles: defaultdict[
                str,
                list[Article],
            ] = defaultdict(list)

            for article in articles:

                source_articles[
                    article.source.name
                ].append(article)

            group_selected: list[Article] = []

            # --------------------------------------------------
            # Apply individual RSS source quotas.
            # --------------------------------------------------

            for source_name, source_quota in RSS_SOURCE_QUOTAS.items():

                source_items = source_articles.get(
                    source_name,
                    [],
                )

                if not source_items:
                    continue

                selected_from_source = source_items[
                    :source_quota
                ]

                group_selected.extend(
                    selected_from_source
                )

                logger.info(
                    "%s → %s: selected %d/%d articles.",
                    group.value,
                    source_name,
                    len(selected_from_source),
                    source_quota,
                )

            # --------------------------------------------------
            # Prevent source quotas from exceeding
            # the SourceGroup quota.
            # --------------------------------------------------

            group_selected = group_selected[
                :group_quota
            ]

            # --------------------------------------------------
            # Identify articles already selected.
            # --------------------------------------------------

            selected_ids = {
                article.id
                for article in group_selected
            }

            # --------------------------------------------------
            # Remaining articles from this source group.
            #
            # These are used to fill unused group slots
            # according to ranking order.
            # --------------------------------------------------

            remaining_group_articles = [
                article
                for article in articles
                if article.id not in selected_ids
            ]

            remaining_slots = (
                group_quota
                - len(group_selected)
            )

            if remaining_slots > 0:

                backfill = remaining_group_articles[
                    :remaining_slots
                ]

                group_selected.extend(
                    backfill
                )

                logger.info(
                    "%s: backfilled %d articles.",
                    group.value,
                    len(backfill),
                )

            # --------------------------------------------------
            # Safety limit.
            # --------------------------------------------------

            group_selected = group_selected[
                :group_quota
            ]

            selected_articles.extend(
                group_selected
            )

            logger.info(
                "%s: selected %d/%d articles.",
                group.value,
                len(group_selected),
                group_quota,
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
                Articles selected after applying quotas.

            ranked_articles:
                All ranked articles.

        Returns:
            Final list of newsletter articles.
        """

        # --------------------------------------------------
        # If the quota selection already reached the
        # newsletter limit, trim and sort by ranking.
        # --------------------------------------------------

        if len(selected_articles) >= NEWSLETTER_TOTAL_ARTICLES:

            selected_articles = selected_articles[
                :NEWSLETTER_TOTAL_ARTICLES
            ]

            selected_articles.sort(
                key=lambda article: article.ranking_score,
                reverse=True,
            )

            logger.info(
                "Newsletter quota already reached maximum "
                "of %d articles.",
                NEWSLETTER_TOTAL_ARTICLES,
            )

            return selected_articles

        # --------------------------------------------------
        # IDs already selected.
        # --------------------------------------------------

        selected_ids = {
            article.id
            for article in selected_articles
        }

        # --------------------------------------------------
        # Find remaining ranked articles.
        # --------------------------------------------------

        remaining_articles = [
            article
            for article in ranked_articles
            if article.id not in selected_ids
        ]

        # --------------------------------------------------
        # Calculate remaining newsletter slots.
        # --------------------------------------------------

        remaining_slots = (
            NEWSLETTER_TOTAL_ARTICLES
            - len(selected_articles)
        )

        # --------------------------------------------------
        # Add highest-ranked remaining articles.
        # --------------------------------------------------

        backfill_articles = remaining_articles[
            :remaining_slots
        ]

        selected_articles.extend(
            backfill_articles
        )

        logger.info(
            "Backfilled %d articles.",
            len(backfill_articles),
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
    LangGraph node responsible for selecting
    the final newsletter articles.
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