"""
Anthropic Collector.

Collects the latest Anthropic news from the
official Anthropic Newsroom.
"""

from __future__ import annotations

from typing import Any

import requests
from bs4 import BeautifulSoup

from agents.collectors.base import BaseCollector

from config.settings import (
    REQUEST_TIMEOUT,
    USER_AGENT,
)

from state.models import (
    Article,
    Source,
    SourceType,
    SourceGroup,
)

from utils.datetime import parse_rss_datetime
from utils.ids import generate_article_id
from utils.logger import get_logger


logger = get_logger(__name__)


class AnthropicCollector(BaseCollector):
    """
    Collect the latest articles from the
    official Anthropic Newsroom.
    """

    NEWSROOM_URL = "https://www.anthropic.com/news"

    MAX_ARTICLES = 2

    def collect(self) -> list[Article]:
        """
        Collect the latest Anthropic articles.

        Returns:
            List of latest Anthropic articles.
        """

        logger.info(
            "Reading Anthropic Newsroom..."
        )

        try:

            response = requests.get(
                self.NEWSROOM_URL,
                timeout=REQUEST_TIMEOUT,
                headers={
                    "User-Agent": USER_AGENT,
                },
            )

            response.raise_for_status()

        except requests.RequestException as exc:

            logger.exception(
                "Failed to fetch Anthropic Newsroom: %s",
                exc,
            )

            return []

        articles = self._parse_newsroom(
            response.text,
        )

        articles.sort(
            key=lambda article: article.published_at,
            reverse=True,
        )

        articles = articles[
            :self.MAX_ARTICLES
        ]

        logger.info(
            "Collected %d latest articles from Anthropic.",
            len(articles),
        )

        return articles

    def _parse_newsroom(
        self,
        html: str,
    ) -> list[Article]:
        """
        Parse Anthropic Newsroom HTML.

        Args:
            html:
                Raw HTML returned by Anthropic.

        Returns:
            Parsed Anthropic articles.
        """

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        articles: list[Article] = []

        # --------------------------------------------------
        # Find article links.
        # --------------------------------------------------

        for link in soup.find_all(
            "a",
            href=True,
        ):

            href = link.get(
                "href",
                "",
            )

            # Only process Anthropic news articles.
            if not href.startswith("/news/"):
                continue

            if href == "/news":
                continue

            title = link.get_text(
                " ",
                strip=True,
            )

            if not title:
                continue

            url = self._build_url(
                href,
            )

            # --------------------------------------------------
            # Avoid duplicate URLs.
            # --------------------------------------------------

            if any(
                article.url == url
                for article in articles
            ):
                continue

            # --------------------------------------------------
            # Try to find publication date.
            # --------------------------------------------------

            published_at = self._extract_date(
                link,
            )

            # If the page does not expose a date in
            # the listing, use current time as fallback.
            if published_at is None:

                from datetime import UTC, datetime

                published_at = datetime.now(
                    UTC,
                )

            source = Source(
                name="Anthropic",
                url=self.NEWSROOM_URL,
                source_type=SourceType.RSS,
                group=SourceGroup.OFFICIAL,
                is_official=True,
                trust_score=1.0,
            )

            article = Article(
                id=generate_article_id(url),
                title=title,
                url=url,
                source=source,
                published_at=published_at,
                summary=None,
                trust_score=1.0,
            )

            articles.append(
                article,
            )

        return articles

    def _extract_date(
        self,
        link: Any,
    ):
        """
        Attempt to extract an article date
        from the surrounding HTML element.
        """

        parent = link.parent

        if parent is None:
            return None

        # Look for <time datetime="...">
        time_element = parent.find(
            "time",
        )

        if time_element:

            date_value = time_element.get(
                "datetime",
            )

            if date_value:

                try:
                    return parse_rss_datetime(
                        date_value,
                    )
                except Exception:
                    pass

        return None

    @staticmethod
    def _build_url(
        href: str,
    ) -> str:
        """
        Convert a relative Anthropic URL
        into an absolute URL.
        """

        if href.startswith("http"):

            return href

        return (
            "https://www.anthropic.com"
            + href
        )


anthropic_collector = AnthropicCollector()


def anthropic_collector_node(
    state: Any,
) -> dict[str, list[Article]]:
    """
    LangGraph node responsible for
    collecting Anthropic news.
    """

    logger.info(
        "Starting Anthropic Collector..."
    )

    articles = anthropic_collector.collect()

    logger.info(
        "Anthropic Collector completed."
    )

    return {
        "articles": articles,
    }