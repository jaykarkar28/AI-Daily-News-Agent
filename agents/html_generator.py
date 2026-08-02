"""
HTML Generator Agent.

Generates a professional HTML newsletter
from the Newsletter object.
"""

from __future__ import annotations

from state.models import (
    Newsletter,
    SourceGroup,
)

from state.news_state import NewsState

from services.html_template import (
    get_html_template,
)

from utils.logger import get_logger

logger = get_logger(__name__)


class HTMLGenerator:
    """
    Generates HTML newsletters.
    """

    def generate(
        self,
        newsletter: Newsletter,
    ) -> str:
        """
        Generate HTML newsletter.
        """

        logger.info(
            "Generating HTML newsletter..."
        )

        content = self._build_content(
            newsletter,
        )

        html = get_html_template()

        html = html.replace(
            "{{TITLE}}",
            newsletter.title,
        )

        html = html.replace(
            "{{DATE}}",
            newsletter.newsletter_date.strftime(
                "%B %d, %Y"
            ),
        )

        html = html.replace(
            "{{CONTENT}}",
            content,
        )

        logger.info(
            "HTML newsletter generated successfully."
        )

        return html

    def _build_content(
        self,
        newsletter: Newsletter,
    ) -> str:
        """
        Build newsletter body.
        """

        html: list[str] = []

        section_titles = {

            SourceGroup.OFFICIAL:
                "🏢 Official Updates",

            SourceGroup.RESEARCH:
                "🧠 Research",

            SourceGroup.OPEN_SOURCE:
                "💻 Open Source",

            SourceGroup.AI_NEWS:
                "📰 AI News",

            SourceGroup.COMMUNITY:
                "🌍 Community",
        }

        grouped: dict[
            SourceGroup,
            list,
        ] = {}

        for article in newsletter.articles:

            grouped.setdefault(
                article.source.group,
                [],
            ).append(article)

        for group in SourceGroup:

            articles = grouped.get(
                group,
                [],
            )

            if not articles:
                continue

            html.append(
                '<div class="section">'
            )

            html.append(
                f'<h2 class="section-title">{section_titles[group]}</h2>'
            )

            for article in articles:

                html.append(
                    '<div class="article">'
                )

                html.append(
                    f"<h3>{article.title}</h3>"
                )

                html.append(
                    '<div class="meta">'
                    f'{article.source.name}'
                    "</div>"
                )

                html.append(
                    f'<div class="summary">'
                    f'{article.summary or "Summary unavailable."}'
                    '</div>'
                )

                html.append(
                    f'<a class="button" '
                    f'href="{article.url}" '
                    f'target="_blank">'
                    'Read More'
                    '</a>'
                )

                html.append(
                    "</div>"
                )

            html.append(
                "</div>"
            )

        return "\n".join(html)


html_generator = HTMLGenerator()


def html_generator_node(
    state: NewsState,
) -> NewsState:
    """
    LangGraph node.
    """

    html = html_generator.generate(
        state["newsletter"],
    )

    return {
        "html_content": html,
    }