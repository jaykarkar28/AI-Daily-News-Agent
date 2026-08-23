"""
Test script for the arXiv Research Collector.
"""

from agents.collectors.arxiv import ArxivCollector


def main() -> None:
    """
    Test arXiv paper collection.
    """

    print("\nStarting arXiv Collector test...\n")

    collector = ArxivCollector()

    articles = collector.collect()

    print(
        f"Total papers collected: {len(articles)}\n"
    )

    for index, article in enumerate(
        articles,
        start=1,
    ):
        print(f"{index}. {article.title}")
        print(
            f"   Published: {article.published_at}"
        )
        print(
            f"   Source: {article.source.name}"
        )
        print(
            f"   Group: {article.source.group}"
        )
        print(f"   URL: {article.url}")
        print(
            f"   Summary: "
            f"{article.summary[:200]}..."
        )
        print("-" * 80)


if __name__ == "__main__":
    main()