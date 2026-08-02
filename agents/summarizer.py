"""
Ai Article Summarizer Agent.
"""

from __future__ import annotations

from state.models import Article
from state.news_state import NewsState

from services.llm_service import llm_service

from utils.logger import get_logger
from utils.prompt_loader import load_prompt


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
    ) -> str:
        """
        Generate an AI summary for a single article.

        Falls back to existing article information
        if the LLM fails or returns an empty response.

        Args:
            article:
                Article to summarize.

        Returns:
            Best available summary.
        """

        prompt = self._build_prompt(
            article,
        )

        summary = llm_service.generate_text(
            prompt,
        )

        # -----------------------------
        # Use LLM summary if valid
        # -----------------------------
        if summary and summary.strip():

            return summary.strip()

        logger.warning(
            "LLM returned an empty summary for: %s",
            article.title,
        )

        # -----------------------------
        # Fallback 1
        # Original article summary
        # -----------------------------
        if article.summary and article.summary.strip():

            return article.summary.strip()

        # -----------------------------
        # Fallback 2
        # First part of article content
        # -----------------------------
        if article.content and article.content.strip():

            return article.content[:400].strip()

        # -----------------------------
        # Final fallback
        # -----------------------------
        return (
            "Summary unavailable. "
            "Please refer to the original article."
        )


    
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





