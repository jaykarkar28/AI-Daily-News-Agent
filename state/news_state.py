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

    search_queries: list[SearchQuery]
    
    # Raw articles collected from all sources.
    articles: Annotated[
        list[Article],
        merge_articles,
    ] 

    # Articles used by the processing pipeline
    # (deduplication, ranking, categorization, summarization).
    processed_articles: list[Article]

    newsletter: Newsletter | None

    execution_info: ExecutionInfo  

    newsletter: Newsletter


