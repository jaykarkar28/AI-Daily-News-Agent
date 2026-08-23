from typing import Any

import feedparser

from agents.collectors.base import BaseCollector
from state.news_state import NewsState
from state.models import (
    Article,
    Source,
    SourceGroup,
    SourceType,
)
from utils.datetime import parse_rss_datetime
from utils.ids import generate_article_id
from utils.logger import get_logger


logger = get_logger(__name__)


class AINewsCollector(BaseCollector):
    """
    Collect major AI industry news from trusted RSS sources.

    Focuses on:
    - AI model and product launches
    - Generative AI developments
    - AI startup funding
    - Major company developments
    - Important AI industry news
    """

    SOURCES: list[dict[str, Any]] = [
        {
            "name": "TechCrunch AI",
            "url": (
                "https://techcrunch.com/category/"
                "artificial-intelligence/feed/"
            ),
            "trust_score": 0.90,
        },
        {
            "name": "VentureBeat AI",
            "url": (
                "https://venturebeat.com/category/ai/feed/"
            ),
            "trust_score": 0.88,
        },
        {
            "name": "MIT Technology Review AI",
            "url": (
                "https://www.technologyreview.com/topic/"
                "artificial-intelligence/feed/"
            ),
            "trust_score": 0.92,
        },
        {
            "name": "The Verge AI",
            "url": (
                "https://www.theverge.com/rss/"
                "ai-artificial-intelligence/index.xml"
            ),
            "trust_score": 0.85,
        },
    ]

    AI_KEYWORDS = [
        "artificial intelligence",
        "generative ai",
        "genai",
        "machine learning",
        "deep learning",
        "large language model",
        "language model",
        "llm",
        "openai",
        "anthropic",
        "claude",
        "chatgpt",
        "gemini",
        "google deepmind",
        "deepmind",
        "meta ai",
        "mistral",
        "hugging face",
        "deepseek",
        "ai model",
        "foundation model",
        "ai agent",
        "agentic",
        "artificial general intelligence",
        "agi",
        "robotics",
    ]

    def __init__(
        self,
        max_articles_per_source: int = 10,
    ) -> None:
        """
        Initialize the AI News Collector.

        Args:
            max_articles_per_source:
                Maximum number of AI-relevant articles
                collected from each source.
        """
        self.max_articles_per_source = (
            max_articles_per_source
        )

    def collect(self) -> list[Article]:
        """
        Collect AI industry news from all configured sources.

        Returns:
            List of normalized AI news Article objects.
        """
        logger.info(
            "Starting AI industry news collection "
            "from %d sources.",
            len(self.SOURCES),
        )

        articles: list[Article] = []

        for source_config in self.SOURCES:

            source_name = source_config["name"]

            try:
                logger.info(
                    "Reading AI news source: %s",
                    source_name,
                )

                parsed_feed = self._fetch_feed(
                    source_config["url"],
                )

                source_articles = self._parse_feed(
                    parsed_feed=parsed_feed,
                    source_config=source_config,
                )

                ai_articles = [
                    article
                    for article in source_articles
                    if self._is_ai_relevant(article)
                ]

                ai_articles.sort(
                    key=lambda article: article.published_at,
                    reverse=True,
                )

                ai_articles = ai_articles[
                    :self.max_articles_per_source
                ]

                logger.info(
                    "Kept %d/%d AI-relevant articles "
                    "from %s.",
                    len(ai_articles),
                    len(source_articles),
                    source_name,
                )

                articles.extend(ai_articles)

            except Exception as error:
                logger.exception(
                    "Failed to collect AI news from %s: %s",
                    source_name,
                    error,
                )

        logger.info(
            "AI News Collector completed. "
            "Total articles collected: %d.",
            len(articles),
        )

        return articles

    def _fetch_feed(
        self,
        url: str,
    ) -> feedparser.FeedParserDict:
        """
        Fetch and parse a single AI news RSS feed.

        Returns:
            Parsed RSS feed. If fetching fails, an empty
            feed is returned so other sources can continue.
        """
        try:
            logger.info(
                "Fetching AI news RSS feed: %s",
                url,
            )

            return feedparser.parse(url)

        except Exception as error:
            logger.exception(
                "Failed to fetch AI news RSS feed: %s. "
                "Error: %s",
                url,
                error,
            )

            return feedparser.FeedParserDict(
                entries=[],
            )

    def _parse_feed(
        self,
        parsed_feed: feedparser.FeedParserDict,
        source_config: dict[str, Any],
    ) -> list[Article]:
        """
        Convert RSS entries into the project's standard
        Article model.
        """
        articles: list[Article] = []

        for entry in parsed_feed.entries:

            try:
                title = entry.get(
                    "title",
                    "Untitled",
                ).strip()

                url = entry.get(
                    "link",
                    "",
                ).strip()

                summary = (
                    entry.get("summary")
                    or entry.get("description")
                    or ""
                ).strip()

                # Skip entries without a usable URL.
                if not url:
                    logger.warning(
                        "Skipping article without URL "
                        "from %s.",
                        source_config["name"],
                    )
                    continue

                # Generate stable article ID.
                article_id = generate_article_id(url)

                # Parse publication date using the project's
                # existing datetime utility.
                published_at = parse_rss_datetime(
                    getattr(
                        entry,
                        "published_parsed",
                        None,
                    )
                )

                # Build the standard Source model.
                source = Source(
                    name=source_config["name"],
                    url=source_config["url"],
                    source_type=SourceType.RSS,
                    group=SourceGroup.AI_NEWS,
                    is_official=False,
                    trust_score=source_config[
                        "trust_score"
                    ],
                )

                # Build the standard Article model.
                article = Article(
                    id=article_id,
                    title=title,
                    url=url,
                    source=source,
                    published_at=published_at,
                    summary=summary,
                    trust_score=source_config[
                        "trust_score"
                    ],
                )

                articles.append(article)

            except Exception:
                # One bad article should not stop the source.
                logger.exception(
                    "Failed to parse AI news article "
                    "from: %s.",
                    source_config["name"],
                )

        return articles

    def _is_ai_relevant(
        self,
        article: Article,
    ) -> bool:
        """
        Check whether an article is relevant to AI.
        """
        content = (
            f"{article.title} {article.summary}"
        ).lower()

        return any(
            keyword in content
            for keyword in self.AI_KEYWORDS
        )


def ai_news_collector_node(
    state: NewsState,
) -> dict[str, Any]:
    """
    LangGraph node for collecting AI industry news.
    """
    logger.info(
        "Starting AI News Collector node.",
    )

    collector = AINewsCollector()

    articles = collector.collect()

    logger.info(
        "AI News Collector node completed. "
        "Collected %d articles.",
        len(articles),
    )

    return {
        "articles": articles,
    }