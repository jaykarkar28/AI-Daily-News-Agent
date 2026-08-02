"""
Newsletter Agent.

Generate the final AI Daily Newsletter from the 
selected and summarized articles.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date

from state.models import (
    Article,
    Newsletter,
    SourceGroup,
)

from state.news_state import NewsState
from utils.logger import get_logger

logger = get_logger(__name__)

class NewsletterGenerator:
    """
    Builds the final newsletter.
    """

    def generate(
        self,
        articles: list[Article],
    ) -> Newsletter:
        """
        Generate the final newsletter.

        Args:
            articles:
                Selected and summarized articles.

        Returns:
            Newsletter object.
        """

        logger.info(
            "Generating Newsletter...."
        )

        grouped_articles = self._group_articles(
            articles,
        )

        markdown = self._build_markdown(
            grouped_articles,
        )

        newsletter = Newsletter(
            title = "AI Daily News",
            newsletter_date=date.today(),
            articles=articles,
            markdown_content=markdown,
        )

        logger.info(
            "Newsletter generated successfully."
        )

        return newsletter

    def _group_articles(
            self,
            articles: list[Article],
    ) -> dict[SourceGroup, list[Article]]:
        """
        Group newsletter articles.

        Articles inside each group are sorted by 
        ranking score in descending order.

        Args:
            articles:
                Selected and newsletter articles.

        Returns:
            Dictionary mapping each SourceGroup
            to its corresponding articles.
        """

        grouped_articles: defaultdict[
            SourceGroup,
            list[Article],
        ] = defaultdict(list)

        for article in articles:
            
            grouped_articles[
                article.source.group
            ].append(article)

        # sort each group by ranking score
        for group_articles in grouped_articles.values():
            
            group_articles.sort(
                key=lambda article: article.ranking_score,
                reverse=True,
            )

        logger.info(
            "Grouped %d newsletter articles into %d sections.",
            len(articles),
            len(grouped_articles),
        )

        return dict(grouped_articles)

    def _build_markdown(
            self,
            grouped_articles: dict[
                SourceGroup,
                list[Article],
            ],
    ) -> str:
        """
        Build the markdown newsletter

        Args:
            grouped_articles:
                Articles grouped by SourceGroup.

        Returns:
            Markdown newsletter.
        """

        markdown: list[str] = []

        # -----------------------
        #  Newsletter header
        # -----------------------

        markdown.append("# 🤖 AI Daily News")

        markdown.append("")

        markdown.append(
            f"**📅 Date:** {date.today():%B %d, %Y}"
        )

        markdown.append("")

        markdown.append(
            "Your daily digest of the most important AI news, "
            "research, open-source projects, and industry updates."
        )

        markdown.append("")

        markdown.append("---")

        markdown.append("")

        # -----------------------
        # Markdown sections
        # -----------------------

        section_titles = {
            SourceGroup.OFFICIAL: "🏢 Official Updates",
            SourceGroup.RESEARCH: "🧠 Research",
            SourceGroup.OPEN_SOURCE: "💻 Open Source",
            SourceGroup.AI_NEWS: "📰 AI News",
            SourceGroup.COMMUNITY: "🌍 Community",
        }

        for group in SourceGroup:

            articles = grouped_articles.get(group, [],)

            if not articles:
                continue

            markdown.append(
                f"## {section_titles[group]}"
            )

            markdown.append("")

            for article in articles:

                markdown.append(
                    f"### 🚀 {article.title}"
                )

                markdown.append("")

                markdown.append(
                    f"🏢 **Source:** {article.source.name}"
                )

                markdown.append("")

                if article.category:

                    markdown.append(
                        f"📂 **Category:** {article.category.value}"
                    )

                    markdown.append("")

                markdown.append(
                    f"📅 **Published:** "
                    f"{article.published_at:%B %d, %Y}"
                )

                markdown.append("")

                markdown.append(
                    "📝 **Summary**"
                )

                markdown.append("")

                markdown.append(
                    article.summary
                    or "Summary unavailable."
                )

                markdown.append("")

                markdown.append(
                    f"🔗 **Read More:** {article.url}"
                )

                markdown.append("")

                markdown.append("---")

                markdown.append("")
                        
        logger.info(
            "Generated markdown newsletter."
        )

        return "\n".join(markdown)

newsletter_generator = NewsletterGenerator()


def newsletter_node(
    state: NewsState,
) -> NewsState:
    """
    Langgraph node responsible for generating 
    the final newsletter
    """

    logger.info(
        "Starting NewsLetter Agent..."
    )

    newsletter = newsletter_generator.generate(
        state["processed_articles"]
    )

    logger.info(
        "Newsletter Agent completed."
    )

    return {
        "newsletter": newsletter,
    }

