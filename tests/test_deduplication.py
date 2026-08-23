from datetime import UTC, datetime

from agents.processing.deduplication import (
    GlobalDeduplicator,
)
from state.models import (
    Article,
    Source,
    SourceGroup,
    SourceType,
)
from utils.ids import generate_article_id


def create_article(
    title: str,
    url: str,
    trust_score: float,
    is_official: bool = False,
) -> Article:
    """
    Create a test article.
    """

    source = Source(
        name="Test Source",
        url="https://example.com",
        source_type=SourceType.WEB_SEARCH,
        group=SourceGroup.AI_NEWS,
        is_official=is_official,
        trust_score=trust_score,
    )

    return Article(
        id=generate_article_id(url),
        title=title,
        url=url,
        source=source,
        summary="Test article summary.",
        published_at=datetime.now(UTC),
        trust_score=trust_score,
    )


def main() -> None:
    """
    Test the GlobalDeduplicator.
    """

    print("Starting Global Deduplication test...\n")

    articles = [

        # ----------------------------------------------
        # URL duplicates
        # ----------------------------------------------

        create_article(
            title="OpenAI launches new AI model",
            url="https://example.com/openai-news",
            trust_score=0.80,
        ),

        create_article(
            title="OpenAI launches new AI model from another source",
            url="https://example.com/openai-news?utm_source=test",
            trust_score=0.90,
        ),

        # ----------------------------------------------
        # Title duplicates
        # ----------------------------------------------

        create_article(
            title="Google announces new Gemini update!",
            url="https://example.com/google-gemini-1",
            trust_score=0.80,
        ),

        create_article(
            title="Google Announces New Gemini Update",
            url="https://another-source.com/gemini-update",
            trust_score=0.95,
        ),

        # ----------------------------------------------
        # Unique articles
        # ----------------------------------------------

        create_article(
            title="New AI agent research released",
            url="https://example.com/ai-agent-research",
            trust_score=0.85,
        ),

        create_article(
            title="Anthropic releases new Claude update",
            url="https://example.com/claude-update",
            trust_score=0.90,
            is_official=True,
        ),
    ]

    print(
        f"Articles before deduplication: {len(articles)}\n"
    )

    deduplicator = GlobalDeduplicator()

    unique_articles = deduplicator.deduplicate(
        articles,
    )

    print(
        f"Articles after deduplication: "
        f"{len(unique_articles)}\n"
    )

    print("Final unique articles:\n")

    for index, article in enumerate(
        unique_articles,
        start=1,
    ):
        print(
            f"{index}. {article.title}"
        )

        print(
            f"   Trust Score: {article.trust_score}"
        )

        print(
            f"   Official: {article.source.is_official}"
        )

        print(
            f"   URL: {article.url}"
        )

        print(
            "-" * 80
        )


if __name__ == "__main__":
    main()