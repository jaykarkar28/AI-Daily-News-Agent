import logging
from typing import Any
import hashlib
from datetime import datetime
import feedparser

from state.news_state import NewsState
from agents.collectors.base import BaseCollector
from config.settings import RSS_FEEDS
from state.models import (
    Article,
    Source,
    SourceType,
)

logger = logging.getLogger(__name__)

class RSSCollector(BaseCollector):
    """
    Collect articles from configured RSS feeds.
    """

    def collect(self) -> list[Article]:
        """
        Collect articles from every configured RSS feed.
        """

        articles: list[Article] = []

        for feed in RSS_FEEDS:

            logger.info("Reading RSS feed: %s", feed["name"])

            parsed_feed = self._fetch_feed(feed["url"])

            articles.extend(
                self._parse_feed(parsed_feed, feed)
            )

        logger.info(
            "Collected %d RSS articles.",
            len(articles)
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
            parsed_feed,
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

                article_id = hashlib.sha256(
                    url.encode("utf-8")
                ).hexdigest()

                # ----------------------------------------------------
                # Parse the publication date.
                # 
                # Some RSS feeds may not provide a valid date.
                # In that case we fall back to the current time.
                # ----------------------------------------------------

                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    
                    published_at = datetime(
                        *entry.published_parsed[:6]
                    )

                else:
                    published_at = datetime.now()

                # ----------------------------
                # Build the Source model.
                # ----------------------------
                source = Source(
                    name=feed_config["name"],
                    url=feed_config["url"],
                    source_type=SourceType.RSS,
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
                # Skip only the current article if coversation fails.
                # The remaining articles should still be processed.
                logger.exception(
                    "Failed to parse RSS article from: '%s'.", 
                    feed_config["name"],
                )
            
        return articles



def rss_collector_node(state: NewsState) -> dict[str, Any]:

    collector = RSSCollector()
    articles = collector.collect()

    return {
        "articles": articles
    }