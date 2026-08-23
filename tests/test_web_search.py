from agents.collectors.web_search import WebSearchCollector


def main() -> None:
    print("\nStarting Web Search Collector test...\n")

    collector = WebSearchCollector()
    articles = collector.collect()

    print(f"Total items collected: {len(articles)}\n")

    if not articles:
        print("No articles were collected.")
        return

    print("Collected articles:\n")

    for index, article in enumerate(articles, start=1):
        print(f"{index}. {article.title}")
        print(f"   Source: {article.source.name}")
        print(f"   Published: {article.published_at}")
        print(f"   URL: {article.url}")
        print("-" * 80)


if __name__ == "__main__":
    main()