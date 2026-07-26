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
