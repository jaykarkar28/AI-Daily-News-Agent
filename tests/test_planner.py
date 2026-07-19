from agents.planner import (
    DEFAULT_QUERIES,
    build_default_queries,
    planner_node,
)
from state.models import(
    ExecutionInfo,
    ExecutionStatus,
    SearchQuery,
)
from state.news_state import NewsState

def test_build_default_queries():
    """ Test default query generation."""

    queries = build_default_queries()

    assert isinstance(queries, list)
    assert len(queries) == len(DEFAULT_QUERIES)

    for query in queries:
        assert isinstance(query, SearchQuery)
        assert query.query != ""
        assert query.target_source is not None
        assert query.priority is not None
        assert query.status is not None

    print("Build default queries test passed.")

def test_planner_node():
    """ Test planner node output."""

    state: NewsState = {
        "search_queries": [],
        "articles": [],
        "newsletter": None,
        "execution_info": ExecutionInfo(
            execution_id="test_execution_001",
            execution_status = ExecutionStatus.PENDING,
        ),
    }

    result = planner_node(state)

    assert isinstance(result, dict)
    assert "search_queries" in result

    queries = result["search_queries"]

    assert isinstance(queries, list)
    assert len(queries) == len(DEFAULT_QUERIES)

    for query in queries:
        assert isinstance(query, SearchQuery)

    print("Planner node test passed.")


if __name__ == "__main__":
    print("="*50)
    print("Planner Tests")
    print("="*50)

    test_build_default_queries()
    test_planner_node()

    print("All planner tests passed successfully")