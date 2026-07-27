from datetime import date, datetime

from state.models import (
    Article,
    Category,
    ExecutionInfo,
    ExecutionStatus,
    Newsletter,
    Priority,
    QueryStatus,
    SearchQuery,
    Source,
    SourceType,
)

from state.news_state import NewsState, merge_articles


def divider(title: str):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ==========================================================
# Create Source
# ==========================================================

source = Source(
    name="OpenAI",
    url="https://openai.com/news",
    source_type=SourceType.OFFICIAL,
    is_official=True,
    trust_score=1.0,
)

# ==========================================================
# Initial State
# ==========================================================

state: NewsState = {
    "search_queries": [],
    "articles": [],
    "newsletter": None,
    "execution_info": ExecutionInfo(
        execution_id="RUN-001",
        execution_status=ExecutionStatus.RUNNING,
    ),
}

divider("Initial State")

print(state)

assert len(state["search_queries"]) == 0
assert len(state["articles"]) == 0
assert state["newsletter"] is None

# ==========================================================
# Planner Node Simulation
# ==========================================================

queries = [
    SearchQuery(
        query="Latest OpenAI News",
        target_source=SourceType.OFFICIAL,
        priority=Priority.HIGH,
        status=QueryStatus.PENDING,
    ),
    SearchQuery(
        query="Latest HuggingFace Models",
        target_source=SourceType.HUGGINGFACE,
        priority=Priority.MEDIUM,
        status=QueryStatus.PENDING,
    ),
]

state["search_queries"] = queries

divider("Planner Finished")

print(f"Queries : {len(state['search_queries'])}")

assert len(state["search_queries"]) == 2

# ==========================================================
# RSS Collector Simulation
# ==========================================================

rss_articles = [
    Article(
        id="001",
        title="GPT-5 Released",
        url="https://openai.com/news",
        source=source,
        published_at=datetime.now(),
        category=Category.MODEL_RELEASE,
    ),
    Article(
        id="002",
        title="OpenAI launches new API",
        url="https://openai.com/api",
        source=source,
        published_at=datetime.now(),
        category=Category.COMPANY_UPDATE,
    ),
]

state["articles"] = merge_articles(
    state["articles"],
    rss_articles,
)

divider("RSS Collector Finished")

print(f"Articles : {len(state['articles'])}")

assert len(state["articles"]) == 2

# ==========================================================
# GitHub Collector Simulation
# ==========================================================

github_articles = [
    Article(
        id="003",
        title="New Open Source AI Framework",
        url="https://github.com",
        source=Source(
            name="GitHub",
            url="https://github.com",
            source_type=SourceType.GITHUB,
            trust_score=0.95,
        ),
        published_at=datetime.now(),
        category=Category.OPEN_SOURCE,
    )
]

state["articles"] = merge_articles(
    state["articles"],
    github_articles,
)

divider("GitHub Collector Finished")

print(f"Articles : {len(state['articles'])}")

assert len(state["articles"]) == 3

# ==========================================================
# Newsletter Generation
# ==========================================================

newsletter = Newsletter(
    title="Daily AI News",
    newsletter_date=date.today(),
    articles=state["articles"],
)

state["newsletter"] = newsletter

divider("Newsletter Generated")

print(state["newsletter"])

assert state["newsletter"] is not None
assert len(state["newsletter"].articles) == 3

# ==========================================================
# Update Execution
# ==========================================================

state["execution_info"].execution_status = ExecutionStatus.COMPLETED
state["execution_info"].completed_at = datetime.now()
state["execution_info"].total_articles = len(state["articles"])

divider("Execution Updated")

print(state["execution_info"])

assert state["execution_info"].execution_status == ExecutionStatus.COMPLETED
assert state["execution_info"].total_articles == 3

# ==========================================================
# Final State
# ==========================================================

divider("Final State Summary")

print(f"Queries           : {len(state['search_queries'])}")
print(f"Articles          : {len(state['articles'])}")
print(f"Newsletter Exists : {state['newsletter'] is not None}")
print(f"Execution Status  : {state['execution_info'].execution_status.value}")

assert len(state["search_queries"]) == 2
assert len(state["articles"]) == 3
assert state["newsletter"] is not None
assert state["execution_info"].execution_status == ExecutionStatus.COMPLETED

divider("ALL TESTS PASSED")

print("NewsState is working correctly.")