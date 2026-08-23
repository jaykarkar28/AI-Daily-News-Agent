"""
Reusable arXiv API clients.

This module handles communication with arXiv and 
return raw research paper results.
"""

from __future__  import annotations

from datetime import UTC
from typing import Any

import arxiv

from config.settings import (
    ARXIV_CATEGORIES,
    ARXIV_MAX_RESULTS,
)

from utils.logger import get_logger

logger = get_logger(__name__)


class ArxivAPI:
    """
    Reusable client for fetching research papers
    from arXiv.
    """
    
    def __init__(self) -> None:
        """
        Initialize the arxiv API client.
        """
        
        self.client = arxiv.Client(
            page_size=ARXIV_MAX_RESULTS,
            delay_seconds=3,
            num_retries=3,
        )
        
    def search_latest_papers(
        self,
    ) -> list[arxiv.Result]:
        """
        Search for the latest papers from the 
        configured AI/ML arXiv categories.
        """
        
        logger.info(
            "Searching arXiv for latest AI/ML research papers."
        )
        
        category_queries = [
            f"cat:{category}"
            for category in ARXIV_CATEGORIES
        ]
        
        query = " OR ".join(category_queries)
        
        search = arxiv.Search(
            query=query,
            max_results=ARXIV_MAX_RESULTS,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )
        
        try:
            results = list(
                self.client.results(search)
            )
            
            logger.info(
                "Fetched %d papers from arXiv.",
                len(results),
            )
            
            return results
        
        except Exception as exc:
            logger.exception(
                "Failed to fetch papers from arXiv: %s",
                exc,
            )
            
            return []
        
    
    @staticmethod
    def result_to_dict(
        result: arxiv.Result,
    ) -> dict[str, Any]:
        """
        Convert an arXiv result to a dictionary.
        """
        
        published_at = result.published
        
        if published_at.tzinfo is not None:
            published_at = published_at.replace(tzinfo=UTC)
            
        else:
            published_at = published_at.astimezone(UTC)
            
        updated_at = result.updated
        
        if updated_at.tzinfo is not None:
            updated_at = updated_at.replace(tzinfo=UTC)
            
        else:
            updated_at = updated_at.astimezone(UTC)
            
        return {
            "title": result.title,
            "url": result.entry_id,
            "summary": result.summary,
            "published_at": published_at,
            "updated_at": updated_at,
            "authors": [author.name for author in result.authors],
            "categories": list(result.categories),
        }
        
        
arxiv_api = ArxivAPI()