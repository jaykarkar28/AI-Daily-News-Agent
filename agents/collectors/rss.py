from typing import Any

import feedparser

from utils.logger import get_logger
from utils.ids import generate_article_id
from utils.datetime import parse_rss_datetime

from state.news_state import NewsState
from datetime import UTC, datetime, timedelta

from agents.collectors.base import BaseCollector
from config.settings import (
    RSS_FEEDS,
    RSS_ARTICLE_MAX_AGE_DAYS,
    RSS_MAX_ARTICLES_PER_FEED,
    RSS_SOURCE_QUOTAS,
)

from state.models import (
    Article,
    Source,
    SourceType,
)

logger = get_logger(__name__)

class RSSCollector(BaseCollector):
    """
    Collect articles from configured RSS feeds.
    """

    def collect(self) -> list[Article]:
        """
        Collect articles from configured RSS feeds.

        OpenAI, Anthropic, and Google DeepMind are limited
        to their latest 2 articles.

        Hugging Face keeps the normal RSS configuration.
        """

        articles: list[Article] = []

        for feed in RSS_FEEDS:

            logger.info(
                "Reading RSS feed: %s",
                feed["name"],
            )

            parsed_feed = self._fetch_feed(
                feed["url"],
            )

            parsed_articles = self._parse_feed(
                parsed_feed,
                feed,
            )

            recent_articles = self._filter_recent_articles(
                parsed_articles,
            )

            # --------------------------------------------------
            # Apply source-specific quota.
            #
            # OpenAI / Anthropic / Google DeepMind:
            # latest 2 articles only.
            #
            # Hugging Face:
            # normal RSS limit.
            # --------------------------------------------------

            source_quota = RSS_SOURCE_QUOTAS.get(
                feed["name"],
            )

            if source_quota is not None:

                recent_articles = recent_articles[
                    :source_quota
                ]

                logger.info(
                    "Applied RSS source quota for %s: "
                    "kept latest %d articles.",
                    feed["name"],
                    len(recent_articles),
                )

            logger.info(
                "Kept %d/%d recent articles from %s.",
                len(recent_articles),
                len(parsed_articles),
                feed["name"],
            )

            articles.extend(
                recent_articles,
            )

        return articles
            
            
    
    def _fetch_feed(self, url: str) -> feedparser.FeedParserDict:
        """
        Download and parse a single RSS feed.

        This method is responsible only for fetching the RSS feed.
        It does not convert the feed into Article objects.

        Args:
            url(str):
                RSS feed URL.

        Returns:
            feedparser.FeedParserDict:
                Parsed RSS feed.
                If the feed cannot be loaded, an empty feed is returned.
        """

        try:
            logger.info("Fetching RSS feed: %s", url)

            # Download and parse the RSS feed
            parsed_feed = feedparser.parse(url)

            return parsed_feed
        
        except Exception as e:
            # We do not stop the workflow if one feed fails.
            # Other RSS feeds should still be processed.
            logger.exception(
                "Failed to fetch RSS feed: %s. Error: %s",
                url,
                e
            )
            # Return an empty feed-like object so the collector can continue processing without raising an exception
            return feedparser.FeedParserDict(entries=[])
    

    def _parse_feed(
            self,
            parsed_feed: feedparser.FeedParserDict,
            feed_config: dict[str, Any],
            ) -> list[Article]:
        
        """
        Convert a parsed RSS feed into a list of Article objects.

        This method is responsible only for transforming RSS entries into the project's standard Article model.

        Args:
            parsed_feed:
                Parsed RSS feed returned by feedparser.

            feed_config:
                Configuration of the RSS source from settings.py.

        Returns:
            list[Article]:
                List of converted articles.
        """

        articles: list[Article] = []

        # Iterate through every article present in the RSS feed
        for entry in parsed_feed.entries:

            try:
                # ----------------------------
                # Extract basic article fields
                # ----------------------------

                title = entry.get("title","Untitled")

                url = entry.get("link","")

                summary = entry.get("summary")

                # --------------------------------------------------
                # Generate a stable unique ID using the article URL.
                # 
                # The same URL will always generate the same ID,
                # preventing duplicate articles across executions.
                # --------------------------------------------------

                article_id = generate_article_id(url)

                # ----------------------------------------------------
                # Parse the publication date.
                # 
                # Some RSS feeds may not provide a valid date.
                # In that case we fall back to the current time.
                # ----------------------------------------------------

                published_at = parse_rss_datetime(
                    getattr(entry, "published_parsed", None)
                )

                # ----------------------------
                # Build the Source model.
                # ----------------------------
                source = Source(
                    name=feed_config["name"],
                    url=feed_config["url"],
                    source_type=SourceType.RSS,
                    group=feed_config["group"],
                    is_official=feed_config["is_official"],
                    trust_score=feed_config["trust_score"],
                )

                # ----------------------------------
                # Create the standard Article object
                # ----------------------------------
                article = Article(
                    id=article_id,
                    title=title,
                    url=url,
                    source=source,
                    published_at=published_at,
                    summary=summary,
                    trust_score=feed_config["trust_score"],
                )

                articles.append(article)
            
            except Exception:
                # Skip only the current article if conversion fails.
                # The remaining articles should still be processed.
                logger.exception(
                    "Failed to parse RSS article from: '%s'.", 
                    feed_config["name"],
                )
            
        return articles
    
    def _filter_recent_articles(
            self,
            articles: list[Article],
    ) -> list[Article]:
        """
        Keep only recent RSS articles.
        
        Articles older than the configured number of days and discarded. The remaining articles are stored from event newest to oldest and limited per RSS feed.
        
        Args:
            articles:
                Articles parsed from a single RSS feed.

        Returns:
            Filtered articles.
        """

        cutoff_date = datetime.now(UTC) - timedelta(
            days = RSS_ARTICLE_MAX_AGE_DAYS,
        )

        # # Temperory debug logs
        # logger.info(
        #     "Cutoff date: %s",
        #     cutoff_date,
        # )

        # for article in articles[:5]:
        #     logger.info(
        #         "Article: %s, Published at: %s",
        #         article.title,
        #         article.published_at,
        #     )

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
            : RSS_MAX_ARTICLES_PER_FEED
        ]






def rss_collector_node(state: NewsState) -> dict[str, Any]:

    collector = RSSCollector()
    articles = collector.collect()

    return {
        "articles": articles
    }