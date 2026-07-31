"""
Categorizer Agent.

Assigns categories to processed AI news articles
using keyword-based classification.
"""

from config.settings import CATEGORY_KEYWORDS

from state.models import (
    Article,
    Category,
)

from state.news_state import NewsState

from utils.logger import get_logger

logger = get_logger(__name__)


class ArticleCategorizer:
    """
    Categorizes AI news articles into predefined categories.
    """

    def categorize_articles(
        self,
        articles: list[Article],
    ) -> list[Article]:
        """
        Categorize all processed articles.

        Args:
            articles: List of processed articles.

        Returns:
            List of categorized articles.
        """

        logger.info(
            "Categorizing %d articles...",
            len(articles),
        )

        categorized_articles = []

        for article in articles:
            article.category = self._calculate_category(article)
            categorized_articles.append(article)

        logger.info(
            "Successfully categorized %d articles.",
            len(categorized_articles),
        )

        return categorized_articles

    def _calculate_category(
        self,
        article: Article,
    ) -> Category:
        """
        Determine the category of a single article.
        """

        search_text = self._build_search_text(article)

        return self._match_category(search_text)

    def _build_search_text(
        self,
        article: Article,
    ) -> str:
        """
        Build searchable text from an article.
        """

        searchable_parts = [
            article.title,
            article.summary or "",
            article.content or "",
            " ".join(article.tags),
        ]

        return " ".join(searchable_parts).lower()

    def _match_category(
        self,
        search_text: str,
    ) -> Category:
        """
        Match article text against configured category keywords.
        """

        for category, keywords in CATEGORY_KEYWORDS.items():

            if any(
                keyword.lower() in search_text
                for keyword in keywords
            ):
                return category

        return Category.OTHER


categorizer = ArticleCategorizer()


def categorizer_node(
    state: NewsState,
) -> NewsState:
    """
    LangGraph node responsible for categorizing articles.
    """

    logger.info("Starting Categorizer Agent...")

    categorized_articles = categorizer.categorize_articles(
        state["processed_articles"]
    )

    logger.info("Categorizer Agent completed.")

    return {
        "processed_articles": categorized_articles,
    }