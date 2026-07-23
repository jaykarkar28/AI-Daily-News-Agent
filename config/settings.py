"""
Application configuration.

All configurable values should live here.
"""

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

REQUEST_TIMEOUT = 15

USER_AGENT = "AI-Daily-News-Agent/1.0"