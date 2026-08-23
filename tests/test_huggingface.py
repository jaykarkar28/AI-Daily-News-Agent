from agents.collectors.huggingface import (
    HuggingFaceCollector,
)


def main() -> None:
    print(
        "Starting Hugging Face Trending Collector test...\n"
    )

    collector = HuggingFaceCollector()

    articles = collector.collect()

    print(
        f"Total items collected: {len(articles)}\n"
    )

    for index, article in enumerate(
        articles,
        start=1,
    ):
        print(f"{index}. {article.title}")
        print(f"   URL: {article.url}")
        print(f"   Source: {article.source.name}")
        print(f"   Group: {article.source.group}")
        print(f"   Summary: {article.summary}")
        print("-" * 80)


if __name__ == "__main__":
    main()