from datetime import datetime

from state.models import (
    Article,
    Source,
    SourceType
)

source = Source(
    name="OpenAI",
    url="https://openai.com/news/",
    source_type=SourceType.OFFICIAL,
    is_official=True,
    trust_score=1.0,
)

article = Article(
    id="001",
    title="GPT-5 Released",
    url="https://openai.com/news/",
    source=source,
    published_at=datetime.now(),
)

print(article)
print(article.model_dump())