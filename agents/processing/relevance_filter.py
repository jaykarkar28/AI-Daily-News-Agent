"""
Article relevance filtering.

Removes low-relevance articles from the global news
collection before ranking and selection.

The filter prioritizes articles related to:

- Major AI companies and organizations
- AI model launches and releases
- Generative AI and LLM developments
- AI agents and agentic systems
- AI research and infrastructure
- Important open-source AI projects

It filters articles that mention AI only incidentally
or are not sufficiently relevant to the AI Daily News
newsletter.
"""

from __future__ import annotations

from typing import Any

from state.models import Article
from state.news_state import NewsState
from utils.logger import get_logger


logger = get_logger(__name__)


class RelevanceFilter:
    """
    Filter articles based on AI relevance.

    Articles receive relevance points based on important
    keywords found in their title and summary.

    An article is kept when its total relevance score
    reaches the configured minimum threshold.
    """

    MIN_RELEVANCE_SCORE = 2

    HIGH_VALUE_KEYWORDS = {
        # Major AI companies
        "openai",
        "anthropic",
        "google deepmind",
        "deepmind",
        "deepseek",
        "xai",
        "mistral ai",
        "hugging face",
        "meta ai",

        # AI models
        "gpt",
        "chatgpt",
        "claude",
        "gemini",
        "llama",
        "qwen",
        "mistral",
        "deepseek-r1",

        # Major AI developments
        "model launch",
        "model release",
        "new model",
        "foundation model",

        # Generative AI
        "generative ai",
        "genai",
        "large language model",
        "llm",
        "multimodal",

        # Agents
        "ai agent",
        "ai agents",
        "agentic ai",
        "agentic",

        # Research
        "machine learning research",
        "artificial intelligence research",
        "ai research",
    }

    MEDIUM_VALUE_KEYWORDS = {
        # General AI terms
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "neural network",

        # AI technology
        "ai model",
        "language model",
        "open source model",
        "open-source model",
        "inference",
        "fine-tuning",
        "finetuning",

        # AI tools
        "rag",
        "retrieval augmented generation",
        "vector database",
        "ai assistant",
        "ai coding",
        "copilot",

        # Infrastructure
        "gpu",
        "ai infrastructure",
        "model training",
    }

    LOW_VALUE_KEYWORDS = {
        "ai",
        "automation",
        "algorithm",
        "data science",
        "robotics",
    }

    def filter(
        self,
        articles: list[Article],
    ) -> list[Article]:
        """
        Filter articles based on AI relevance.

        Args:
            articles:
                Articles after global deduplication.

        Returns:
            Articles that meet the minimum relevance score.
        """

        logger.info(
            "Starting relevance filtering for %d articles.",
            len(articles),
        )

        if not articles:
            return []

        relevant_articles: list[Article] = []

        for article in articles:

            relevance_score = self._calculate_relevance_score(
                article,
            )

            if relevance_score >= self.MIN_RELEVANCE_SCORE:
                relevant_articles.append(
                    article,
                )
            else:
                logger.debug(
                    "Filtered low-relevance article: %s | Score: %d",
                    article.title,
                    relevance_score,
                )

        removed_count = (
            len(articles)
            - len(relevant_articles)
        )

        logger.info(
            "Relevance filtering completed: %d -> %d articles. "
            "Removed %d low-relevance articles.",
            len(articles),
            len(relevant_articles),
            removed_count,
        )

        return relevant_articles

    # --------------------------------------------------
    # Relevance Scoring
    # --------------------------------------------------

    def _calculate_relevance_score(
        self,
        article: Article,
    ) -> int:
        """
        Calculate AI relevance score for one article.

        Title matches receive more importance than
        summary matches.
        """

        title = (
            article.title
            or ""
        ).lower()

        summary = (
            article.summary
            or ""
        ).lower()

        score = 0

        # High-value keywords.
        score += self._score_keywords(
            text=title,
            keywords=self.HIGH_VALUE_KEYWORDS,
            points=3,
        )

        score += self._score_keywords(
            text=summary,
            keywords=self.HIGH_VALUE_KEYWORDS,
            points=1,
        )

        # Medium-value keywords.
        score += self._score_keywords(
            text=title,
            keywords=self.MEDIUM_VALUE_KEYWORDS,
            points=2,
        )

        score += self._score_keywords(
            text=summary,
            keywords=self.MEDIUM_VALUE_KEYWORDS,
            points=1,
        )

        # Low-value keywords.
        score += self._score_keywords(
            text=title,
            keywords=self.LOW_VALUE_KEYWORDS,
            points=1,
        )

        return score

    def _score_keywords(
        self,
        text: str,
        keywords: set[str],
        points: int,
    ) -> int:
        """
        Calculate keyword relevance points.

        Each keyword contributes only once.
        """

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += points

        return score


# --------------------------------------------------
# LangGraph Node
# --------------------------------------------------

def relevance_filter_node(
    state: NewsState,
) -> dict[str, Any]:
    """
    LangGraph node that filters articles based
    on AI relevance.
    """

    articles = state.get(
        "articles",
        [],
    )

    logger.info(
        "Relevance Filter node received %d articles.",
        len(articles),
    )

    relevance_filter = RelevanceFilter()

    filtered_articles = relevance_filter.filter(
        articles,
    )

    logger.info(
        "Relevance Filter node returning %d articles.",
        len(filtered_articles),
    )

    return {
        "articles": filtered_articles,
    }