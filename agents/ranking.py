"""
Global Article Ranking Node
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from config.settings import(
    RANKING_TRUST_WEIGHT,
    RANKING_FRESHNESS_WEIGHT,
    RANKING_KEYWORD_WEIGHT, 
    RANKING_KEYWORDS,
    FRESHNESS_MAX_DAYS,
)

from state.models import Article
from state.news_state import NewsState
from utils.logger import get_logger

logger = get_logger(__name__)

class ArticleRanker:
    """
    Calculates ranking scores for collected articles.
    """

    def rank_articles(
        self,
        articles: list[Article],
    ) -> list[Article]:
        
        logger.info(
            "Ranking %d collected articles.",
            len(articles),
        )

        for article in articles:
            article.ranking_score = self._calculate_score(article)

        ranked_articles = self._sort_articles(articles)

        if ranked_articles:
            logger.info(
                "Top ranked article: %s (score: %.3f)",
                ranked_articles[0].title,
                ranked_articles[0].ranking_score,
            )

        logger.info(
            "Ranking Completed."
        )

        return ranked_articles

    
    def _calculate_score(
            self,
            article: Article,
    ) -> float:

        trust = self._calculate_trust_score(article)
        freshness = self._calculate_freshness_score(article)
        keyword = self._calculate_keyword_score(article)

        score = (
            trust * RANKING_TRUST_WEIGHT +
            freshness * RANKING_FRESHNESS_WEIGHT +
            keyword * RANKING_KEYWORD_WEIGHT
        )

        return round(score, 3)
    
    def _calculate_trust_score(
            self,
            article: Article,
    ) -> float:

        return article.source.trust_score

    def _calculate_freshness_score(
            self,
            article: Article,
    ) -> float:

        age = (datetime.now() - article.published_at).days  

        score = max(
            0.0,
            1.0 - (age / FRESHNESS_MAX_DAYS)
        )

        return score
    
    def _calculate_keyword_score(
            self,
            article: Article,
    ) -> float:

        search_text = (
            article.title.lower()
            + " "
            + " ".join(article.tags).lower()
        )

        best_score = 0.0

        for keyeord, score in RANKING_KEYWORDS.items():
            if keyeord in search_text:
                best_score = max(best_score, score)

        return best_score
    
    def _sort_articles(
            self,
            articles: list[Article],
    ) -> list[Article]:

        return sorted(
            articles,
            key = lambda article: article.ranking_score,
            reverse = True
        )


def ranking_node(
        state: dict[str, Any]
) -> dict[str, Any]:

    """
    Global article ranking node.
    """

    logger.info("Ranking node started.")

    ranker = ArticleRanker()

    ranked_articles = ranker.rank_articles(state["articles"])

    return{
        **state,
        "articles": ranked_articles,
    }