from datetime import UTC, datetime, timedelta
from typing import Any
from email.utils import parsedate_to_datetime

from tavily import TavilyClient

from agents.collectors.base import BaseCollector
from config.settings import (
    TAVILY_API_KEY,
    WEB_SEARCH_MAX_RESULTS,
    WEB_SEARCH_MAX_AGE_DAYS,
    WEB_SEARCH_MAX_ARTICLES,
    WEB_SEARCH_TRUST_SCORE,
    WEB_SEARCH_QUERIES,
)
from state.models import (
    Article,
    Source,
    SourceGroup,
    SourceType,
)
from state.news_state import NewsState
from utils.ids import generate_article_id
from utils.logger import get_logger


logger = get_logger(__name__)


class WebSearchCollector(BaseCollector):
    """
    Collect recent AI news using web search.

    The collector searches for:
    - General AI news
    - AI model launches
    - Generative AI updates
    - AI agent developments

    Results are converted into the project's
    standard Article model.
    """

    def __init__(self) -> None:
        """
        Initialize the Tavily search client.
        """

        if not TAVILY_API_KEY:
            raise ValueError(
                "TAVILY_API_KEY is not configured."
            )

        self.client = TavilyClient(
            api_key=TAVILY_API_KEY,
        )

    def collect(self) -> list[Article]:
        """
        Collect AI news from all configured
        web search queries.
        """

        articles: list[Article] = []

        logger.info(
            "Starting Web Search AI news collection."
        )

        for query in WEB_SEARCH_QUERIES:

            logger.info(
                "Searching web for query: %s",
                query,
            )

            query_articles = self._search_query(
                query=query,
            )

            articles.extend(
                query_articles,
            )

        # Remove duplicate URLs.
        articles = self._deduplicate_articles(
            articles,
        )

        # Keep only recent articles.
        articles = self._filter_recent_articles(
            articles,
        )

        # Sort newest first.
        articles.sort(
            key=lambda article: article.published_at,
            reverse=True,
        )

        # Apply total collector limit.
        articles = articles[
            :WEB_SEARCH_MAX_ARTICLES
        ]

        logger.info(
            "Total Web Search AI news articles collected: %d",
            len(articles),
        )

        return articles

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    def _search_query(
        self,
        query: str,
    ) -> list[Article]:
        """
        Execute one web search query and convert
        the results into Article objects.
        """

        articles: list[Article] = []

        try:
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=WEB_SEARCH_MAX_RESULTS,
                topic="news",
                days=WEB_SEARCH_MAX_AGE_DAYS,
            )

            results = response.get(
                "results",
                [],
            )

            logger.info(
                "Web search returned %d results for query: %s",
                len(results),
                query,
            )

            for result in results:

                try:
                    article = self._convert_result_to_article(
                        result=result,
                    )

                    if article is not None:
                        articles.append(
                            article,
                        )

                except Exception:
                    logger.exception(
                        "Failed to convert web search result."
                    )

        except Exception:
            logger.exception(
                "Web search failed for query: %s",
                query,
            )

        return articles

    # --------------------------------------------------
    # Result Conversion
    # --------------------------------------------------

    def _convert_result_to_article(
        self,
        result: dict[str, Any],
    ) -> Article | None:
        """
        Convert one Tavily search result into
        the standard Article model.
        """

        title = (
            result.get("title")
            or "Untitled AI News"
        )

        url = result.get(
            "url",
            "",
        )

        summary = (
            result.get("content")
            or result.get("snippet")
            or ""
        )

        # Skip results without a usable URL.
        if not url:
            return None

        published_at = self._parse_published_date(
            result=result,
        )

        source_name = self._extract_source_name(
            url=url,
        )

        source = Source(
            name=source_name,
            url=url,
            source_type=SourceType.WEB_SEARCH,
            group=SourceGroup.AI_NEWS,
            is_official=False,
            trust_score=WEB_SEARCH_TRUST_SCORE,
        )

        return Article(
            id=generate_article_id(url),
            title=title,
            url=url,
            source=source,
            summary=summary,
            published_at=published_at,
            trust_score=WEB_SEARCH_TRUST_SCORE,
        )

    # --------------------------------------------------
    # Date Parsing
    # --------------------------------------------------

    def _parse_published_date(
        self,
        result: dict[str, Any],
    ) -> datetime:
        """
        Parse the publication date returned
        by the search provider.

        Supports:
        - ISO-8601 dates
        - RFC/RSS-style dates

        Falls back to the current UTC time
        if a valid date is unavailable.
        """

        raw_date = result.get(
            "published_date",
        )

        if not raw_date:
            return datetime.now(UTC)

        try:
            # ------------------------------------------
            # Try ISO-8601 format first.
            # Example:
            # 2026-08-21T13:55:49Z
            # ------------------------------------------

            parsed_date = datetime.fromisoformat(
                raw_date.replace(
                    "Z",
                    "+00:00",
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            try:
                # ------------------------------------------
                # Try RFC/RSS format.
                # Example:
                # Fri, 21 Aug 2026 13:55:49 GMT
                # ------------------------------------------

                parsed_date = parsedate_to_datetime(
                    raw_date,
                )

            except (
                TypeError,
                ValueError,
            ):

                logger.warning(
                    "Could not parse web search date: %s",
                    raw_date,
                )

                return datetime.now(UTC)

        # Ensure timezone-aware UTC datetime.
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(
                tzinfo=UTC,
            )

        return parsed_date.astimezone(UTC)

    # --------------------------------------------------
    # Source Name
    # --------------------------------------------------

    def _extract_source_name(
        self,
        url: str,
    ) -> str:
        """
        Extract a readable source name
        from an article URL.
        """

        try:
            domain = (
                url.split("//", 1)[-1]
                .split("/", 1)[0]
            )

            return domain.replace(
                "www.",
                "",
            )

        except Exception:
            return "Web Search"

    # --------------------------------------------------
    # Deduplication
    # --------------------------------------------------

    def _deduplicate_articles(
        self,
        articles: list[Article],
    ) -> list[Article]:
        """
        Remove duplicate articles based on URL.
        """

        seen_urls: set[str] = set()

        unique_articles: list[Article] = []

        for article in articles:

            if article.url in seen_urls:
                continue

            seen_urls.add(
                article.url,
            )

            unique_articles.append(
                article,
            )

        logger.info(
            "Web Search deduplication: %d unique articles remain.",
            len(unique_articles),
        )

        return unique_articles

    # --------------------------------------------------
    # Recency Filtering
    # --------------------------------------------------

    def _filter_recent_articles(
        self,
        articles: list[Article],
    ) -> list[Article]:
        """
        Keep only articles within the configured
        maximum age.
        """

        cutoff_date = (
            datetime.now(UTC)
            - timedelta(
                days=WEB_SEARCH_MAX_AGE_DAYS,
            )
        )

        recent_articles = [
            article
            for article in articles
            if article.published_at >= cutoff_date
        ]

        logger.info(
            "Web Search recency filter: kept %d/%d articles.",
            len(recent_articles),
            len(articles),
        )

        return recent_articles


# --------------------------------------------------
# LangGraph Node
# --------------------------------------------------

def web_search_collector_node(
    state: NewsState,
) -> dict[str, Any]:
    """
    LangGraph node for the Web Search Collector.
    """

    collector = WebSearchCollector()

    articles = collector.collect()

    logger.info(
        "Web Search Collector node collected %d articles.",
        len(articles),
    )

    return {
        "articles": articles,
    }