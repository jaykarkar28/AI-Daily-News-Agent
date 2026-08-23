"""
Test script for the AI News Collector.
"""

from agents.collectors.ai_news import AINewsCollector


def main() -> None:
    print(
        "Starting AI News Collector test...\n"
    )

    collector = AINewsCollector()

    articles = collector.collect()

    print(
        f"Total AI news articles collected: "
        f"{len(articles)}\n"
    )

    for index, article in enumerate(
        articles,
        start=1,
    ):
        print(f"{index}. {article.title}")
        print(
            f"   Published: "
            f"{article.published_at}"
        )
        print(
            f"   Source: "
            f"{article.source.name}"
        )
        print(
            f"   Group: "
            f"{article.source.group}"
        )
        print(f"   URL: {article.url}")
        print(
            f"   Summary: "
            f"{article.summary[:200]}..."
        )
        print("-" * 80)


if __name__ == "__main__":
    main()