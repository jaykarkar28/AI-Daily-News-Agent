"""
Application configuration.

All configurable values should live here.
"""

# ------------------------------
# RSS CONFIGURATION
# ------------------------------
RSS_FEEDS = [
    {
        "name": "OpenAI",
        "url": "https://openai.com/news/rss.xml",
        "trust_score": 1.0,
        "is_official": True,
    },
    {
        "name": "Google DeepMind",
        "url": "https://blog.google/technology/ai/rss/",
        "trust_score": 0.95,
        "is_official": True,
    },
    {
        "name": "Hugging Face",
        "url": "https://huggingface.co/blog/feed.xml",
        "trust_score": 0.95,
        "is_official": True,
    },
]

# Keep RSS articles published within the last N days.
RSS_ARTICLE_MAX_AGE_DAYS = 7

# Maximum number of articles to keep from each RSS feed.
RSS_MAX_ARTICLES_PER_FEED = 20

REQUEST_TIMEOUT = 15

USER_AGENT = "AI-Daily-News-Agent/1.0"

# ------------------------------
# Github Configuration
# ------------------------------

GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_API_VERSION = "2022-11-28"
GITHUB_REPOSITORIES_PER_QUERY = 10
GITHUB_TRUST_SCORE = 0.9


# ------------------------------
# Ranking Configuration
# ------------------------------

RANKING_TRUST_WEIGHT = 0.40
RANKING_FRESHNESS_WEIGHT = 0.30
RANKING_KEYWORD_WEIGHT = 0.30

RANKING_KEYWORDS = {
    "gpt": 1.0,
    "openai": 1.0,
    "gemini": 1.0,
    "claude": 1.0,
    "anthropic": 0.95,
    "deepmind": 0.95,
    "llama": 0.90,
    "langgraph": 0.90,
    "langchain": 0.85,
    "agent": 0.80,
    "reasoning": 0.80,
    "mcp": 0.75,
}

FRESHNESS_MAX_DAYS = 7
RANKING_MAX_ARTICLES = 50
