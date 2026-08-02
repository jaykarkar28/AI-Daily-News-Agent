from typing import Annotated, TypedDict

from state.models import(
    Article,
    ExecutionInfo,
    Newsletter,
    SearchQuery
)

def merge_articles(
        current: list[Article],
        new: list[Article],
) -> list[Article]:
    """
    Merge newly collecoted articles into the existing list.
    """
    return current + new


class NewsState(TypedDict):
    """
    Shared workflow state for the AI Daily News Agent.

    Every LangGraph node receives this state,
    reads the data it needs,
    updates its own fields,
    and returns the updated state.
    """

    # Planner
    search_queries: list[SearchQuery]

    # Raw articles collected from all collectors
    articles: Annotated[
        list[Article],
        merge_articles,
    ]

    # Processed articles flowing through the pipeline
    processed_articles: list[Article]

    # Generated newsletter
    newsletter: Newsletter

    # Saved newsletter file path
    output_path: str

    # Workflow metadata
    execution_info: ExecutionInfo


