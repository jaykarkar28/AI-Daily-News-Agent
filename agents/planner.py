"""
Responsibilities

The Planner node should:

Decide what to search.
Decide where to search.
Prioritize searches.
Create SearchQuery objects.

It should not:

Fetch articles.
Call APIs.
Generate newsletters.
Categorize content.

"""
import logging
from typing import Any  

from state.news_state import NewsState
from state.models import (
    SearchQuery,
    SourceType,
    Priority,
)

logger = logging.getLogger(__name__)


#------------  Default Search Defination ------------

DEFAULT_QUERIES = [
    ("Latest OpenAI announcements", SourceType.OFFICIAL, Priority.HIGH),
    ("Latest Anthropic announcements", SourceType.OFFICIAL, Priority.HIGH),
    ("Latest Google Gemini AI updates", SourceType.OFFICIAL, Priority.HIGH),
    ("Latest Hugging Face models", SourceType.HUGGINGFACE, Priority.HIGH),
    ("Trending AI Github repositories", SourceType.GITHUB, Priority.HIGH),
    ("Latest AI research papers", SourceType.ARXIV, Priority.MEDIUM),
    ("Latest AI news", SourceType.RSS, Priority.MEDIUM),
]


def build_default_queries() -> list[SearchQuery]:
    """
    Build the default list of  search queries.

    Returns:
    list[SearchQuery]: List of planner-generated queries.
    """

    queries = []

    for query, source, priority in DEFAULT_QUERIES:
        queries.append(
            SearchQuery(
                query=query,
                target_source=source,
                priority=priority,
            )
        )

    return queries


def planner_node(state: NewsState) -> dict[str, Any]:
    """
    The planner node for the AI Daily News workflow.

    Responsibilities:
    - Generate search queries.
    - Return only the updated portion of the workflow state.

    Args:
        state (NewsState): Current workflow state.

    Returns:
        dict: Partial  state update  containing search queries.
    """

    logger.info("Planner node started.")
    
    queries = build_default_queries()

    logger.info(
        "Planner generated %d search queries.",
        len(queries)
    )

    return {
        "search_queries": queries
    }
