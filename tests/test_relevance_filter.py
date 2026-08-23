"""
Test the AI article relevance filter.
"""

from datetime import UTC, datetime

from agents.processing.relevance_filter import (
    RelevanceFilter,
)
from state.models import (
    Article,
    Source,
    SourceGroup,
    SourceType,
)


def create_article(
    article_id: str,
    title: str,
    summary: str,
) -> Article:
    """
    Create a test article.
    """

    source = Source(
        name="Test Source",
        url="https://example.com",
        source_type=SourceType.WEB_SEARCH,
        group=SourceGroup.AI_NEWS,
        is_official=False,
        trust_score=0.8,
    )

    return Article(
        id=article_id,
        title=title,
        url=f"https://example.com/{article_id}",
        source=source,
        summary=summary,
        published_at=datetime.now(UTC),
        trust_score=0.8,
    )


def main() -> None:
    """
    Run relevance filter tests.
    """

    print("Starting Relevance Filter test...")
    print()

    articles = [
        # Should be kept: major AI company/model.
        create_article(
            article_id="article-1",
            title="OpenAI launches a new GPT model",
            summary=(
                "OpenAI announced a major new foundation "
                "model with improved reasoning capabilities."
            ),
        ),

        # Should be kept: AI agents.
        create_article(
            article_id="article-2",
            title="AI agents are transforming enterprise workflows",
            summary=(
                "New agentic AI systems are being adopted "
                "by large companies."
            ),
        ),

        # Should be kept: strong AI research relevance.
        create_article(
            article_id="article-3",
            title="New machine learning research improves model training",
            summary=(
                "Researchers developed a new deep learning "
                "training technique."
            ),
        ),

        # Should be kept: medium AI relevance.
        create_article(
            article_id="article-4",
            title="New AI infrastructure improves GPU inference",
            summary=(
                "The new platform helps accelerate "
                "machine learning workloads."
            ),
        ),

        # Should be filtered: only weak AI mention.
        create_article(
            article_id="article-5",
            title="Company announces new business strategy",
            summary=(
                "The company mentioned AI as one of several "
                "technologies it may explore in the future."
            ),
        ),

        # Should be filtered: unrelated.
        create_article(
            article_id="article-6",
            title="Local football team wins championship",
            summary=(
                "Fans celebrated after an exciting final match."
            ),
        ),

        # Should be filtered: weak automation mention only.
        create_article(
            article_id="article-7",
            title="Company improves office automation process",
            summary=(
                "The organization introduced new workflow "
                "tools for employees."
            ),
        ),
    ]

    relevance_filter = RelevanceFilter()

    print(
        f"Articles before filtering: {len(articles)}"
    )
    print()

    filtered_articles = relevance_filter.filter(
        articles,
    )

    print(
        f"Articles after filtering: {len(filtered_articles)}"
    )
    print()

    print("Relevant articles:")

    for index, article in enumerate(
        filtered_articles,
        start=1,
    ):
        score = relevance_filter._calculate_relevance_score(
            article,
        )

        print()
        print(
            f"{index}. {article.title}"
        )
        print(
            f"   Relevance Score: {score}"
        )
        print(
            f"   Summary: {article.summary}"
        )
        print("-" * 80)

    # Expected result.
    expected_count = 4

    assert len(filtered_articles) == expected_count, (
        f"Expected {expected_count} articles, "
        f"but got {len(filtered_articles)}."
    )

    print()
    print(
        "Relevance Filter test completed successfully!"
    )


if __name__ == "__main__":
    main()