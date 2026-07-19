from datetime import date, datetime

from state.models import (
    Article,
    Category,
    ExecutionInfo,
    Newsletter,
    Priority,
    SearchQuery,
    Source,
    SourceType,
)

print("=" * 60)
print("Testing Source")
print("=" * 60)

source = Source(
    name="OpenAI",
    url="https://openai.com/news/",
    source_type=SourceType.OFFICIAL,
    is_official=True,
)

print(source)

print("\n")

print("=" * 60)
print("Testing Article")
print("=" * 60)

article = Article(
    id="001",
    title="GPT-5 Released",
    url="https://openai.com/news/",
    source=source,
    published_at=datetime.now(),
    category=Category.MODEL_RELEASE,
)

print(article)

print("\n")

print("=" * 60)
print("Testing SearchQuery")
print("=" * 60)

query = SearchQuery(
    query="Latest OpenAI News",
    target_source=SourceType.OFFICIAL,
    priority=Priority.HIGH,
)

print(query)

print("\n")

print("=" * 60)
print("Testing Newsletter")
print("=" * 60)

newsletter = Newsletter(
    title="AI Daily News",
    newsletter_date=date.today(),
    articles=[article],
)

print(newsletter)

print("\n")

print("=" * 60)
print("Testing ExecutionInfo")
print("=" * 60)

execution = ExecutionInfo(
    execution_id="RUN-20260719-001"
)

print(execution)

print("\n")

print("=" * 60)
print("Serialized Newsletter")
print("=" * 60)

print(newsletter.model_dump())

print("\n")

print("=" * 60)
print("All Model Tests Passed Successfully!")
print("=" * 60)