#  -------------------- UPDATED -------------------------


"""
HTML Generator Agent.

Generates a professional HTML newsletter
from the Newsletter object.
"""

from __future__ import annotations
from datetime import datetime

from html import escape

from state.models import (
    Article,
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
        Generate the complete HTML newsletter.
        """

        logger.info(
            "Generating HTML newsletter..."
        )

        content = self._build_content(
            newsletter,
        )

        stats = self._build_statistics(
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
            "{{STATS}}",
            stats,
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
        Build newsletter sections.
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
        
        section_colors = {
            SourceGroup.OFFICIAL: "#2563EB",
            SourceGroup.RESEARCH: "#7C3AED",
            SourceGroup.OPEN_SOURCE: "#16A34A",
            SourceGroup.AI_NEWS: "#EA580C",
            SourceGroup.COMMUNITY: "#0891B2",
        }

        grouped: dict[
            SourceGroup,
            list[Article],
        ] = {}

        for article in newsletter.articles:

            grouped.setdefault(
                article.source.group,
                [],
            ).append(article)

        # Sort articles inside each section
        for articles in grouped.values():

            articles.sort(
                key=lambda article: article.ranking_score,
                reverse=True,
            )

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
            
            color = section_colors[group]

            html.append(
                f'''
                <h2
                    class="section-title"
                    style="
                        color:{color};
                        border-left-color:{color};
                    "
                >
                {section_titles[group]}
                </h2>
                '''
                )

            for article in articles:

                html.append(
                    self._build_article_card(
                        article,
                    )
                )

            html.append(
                "</div>"
            )

        return "\n".join(html)

    def _build_article_card(
        self,
        article: Article,
    ) -> str:
        """
        Build a single article card.
        """

        title = escape(
            article.title
        )

        summary = escape(
            article.summary
            or "Summary unavailable."
        )

        source = escape(
            article.source.name
        )

        category = (
            article.category.value
            if article.category
            else "General"
        )

        published = article.published_at.strftime(
            "%B %d, %Y"
        )

        if article.ranking_score:

            if article.ranking_score >= 0.90:
                score = "🟢 Excellent"

            elif article.ranking_score >= 0.75:
                score = "🟡 High"

            elif article.ranking_score >= 0.60:
                score = "🟠 Medium"

            else:
                score = "⚪ Low"

        else:
            score = "-"

        if (
            article.source.group
            == SourceGroup.OPEN_SOURCE
        ):

            button = "💻 View Repository →"

        else:

            button = "📖 Read Full Article →"

        return f"""

            <div class="article">

            <h3>

            🚀 {title}

            </h3>

            <div class="badges">

            <span class="badge source">

            🏢 {source}

            </span>

            <span class="badge category">

            📂 {category}

            </span>

            <span class="badge date">

            📅 {published}

            </span>

            <span class="badge score">

            {score}

            </span>

            </div>

            <div class="summary">

            {summary}

            </div>

            <a
                class="button"
                href="{article.url}"
                target="_blank"
            >

            {button}

            </a>

            </div>

            """
            
    def _build_statistics(
        self,
        newsletter: Newsletter,
    ) -> str:
            """
            Build the statistics dashboard.
            """

            total_articles = len(
                newsletter.articles
            )

            total_sections = len(
                {
                    article.source.group
                    for article in newsletter.articles
                }
            )

            official = sum(
                1
                for article in newsletter.articles
                if article.source.group
                == SourceGroup.OFFICIAL
            )

            open_source = sum(
                1
                for article in newsletter.articles
                if article.source.group
                == SourceGroup.OPEN_SOURCE
            )
            
            generated_time = datetime.now().strftime(
                "%b %d, %Y • %I:%M %p"
            )

            return f"""

    <div class="stats">

    <div class="stat-card">
        <div class="stat-title">
            📰 Articles
        </div>
        <div class="stat-value">
            {total_articles}
        </div>
    </div>

    <div class="stat-card">
        <div class="stat-title">
            📂 Sections
        </div>
        <div class="stat-value">
            {total_sections}
        </div>
    </div>

    <div class="stat-card">
        <div class="stat-title">
            🏢 Official
        </div>
        <div class="stat-value">
            {official}
        </div>
    </div>

    <div class="stat-card">
        <div class="stat-title">
            💻 Open Source
        </div>
        <div class="stat-value">
            {open_source}
        </div>
    </div>

    <div class="stat-card">
        <div class="stat-title">
            🕒 Generated
        </div>
        <div class="stat-value">
            {generated_time}
        </div>
    </div>

</div>

    """


html_generator = HTMLGenerator()


def html_generator_node(
    state: NewsState,
) -> NewsState:
    """
    LangGraph node responsible for
    generating the HTML newsletter.
    """

    logger.info(
        "Starting HTML Generator..."
    )

    html = html_generator.generate(
        state["newsletter"],
    )

    logger.info(
        "HTML Generator completed."
    )

    return {
        "html_content": html,
    }