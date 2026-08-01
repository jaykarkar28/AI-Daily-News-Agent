"""
Ai Article Summarizer Agent.
"""

from __future__ import annotations

from state.models import Article
from state.news_state import NewsState

from services.llm_service import llm_service

from utils.logger import get_logger
from utils.prompt_loader import load_prompt
from config.settings import (
    SUMMARY_MAX_ARTICLES,
)

logger = get_logger(__name__)


class ArticleSummarizer:
    """
    Generates AI summaries for processed articles.
    """

    def summarize_articles(
            self,
            articles: list[Article],
    ) -> list[Article]:
        """
        Generate Summaries for all processed articles.
        
        Args:
            articles:
                Ranked and categorized articles.
        
        Returns:
            Articles with generated summaries.
        """

        articles = articles[:SUMMARY_MAX_ARTICLES]

        logger.info(
            "Summarizing %d articles...",
            len(articles),
        )


        summarized_articles = []

        for index, article in enumerate(
            articles,
            start=1,
        ):
        
            logger.info(
                "[%d/%d] Summarizing article: %s",
                index,
                len(articles),
                article.title,
            )

            article.summary = self._summarize_article(
                article,
            )

            summarized_articles.append(article)

            if article.summary:

                logger.info(
                    "Summarized: %s",
                    article.title,
                )

            else:

                logger.info(
                    "Skipped: %s",
                    article.title,
                )

        successful = sum(
            1 for article in summarized_articles 
            if article.summary
        )

        logger.info(
            "Successfully summarized %d/%d articles.",
            successful,
            len(summarized_articles),
        )

        return summarized_articles

    
    def _summarize_article(
        self,
        article: Article,
    ) -> str | None:
        """
        Generate an AI summary for a single article.
        
        Args:
            article:
                Article to summarize.

        Returns:
            Generated summary or None if generation fails.
        """

        prompt = self._build_prompt(article)

        summary = llm_service.generate_text(prompt)

        if summary is None or not summary.strip():

            logger.warning(
                "Empty summary returned for article: %s",
                article.title,
            )

            return None
        
        return summary.strip()
    
    def _build_prompt(
            self,
            article: Article,
    ) -> str:
        """
        Build the final prompt sent to the LLM.
        
        Args:
            article:
                Article to summarize.

        Returns:
            Formatted prompt.
        """

        prompt = load_prompt("summarizer.md")

        prompt = prompt.replace(
            '{title}',
            article.title,
        )

        prompt = prompt.replace(
            '{content}',
            article.content 
            or article.summary
            or "No additional content available.",
        )

        return prompt


summarizer = ArticleSummarizer()


def summarize_node(
        state: NewsState,
) -> NewsState:
    """
    Langgraph node responsible for generating AI summaries for processed articles
    """

    logger.info(
        "Starting Summarizer Agent..."
    )

    summarized_articles = summarizer.summarize_articles(
        state["processed_articles"]
    )

    logger.info(
        "Summarizer Agent completed."
    )

    return{
        **state,
        "processed_articles": summarized_articles,
    }





