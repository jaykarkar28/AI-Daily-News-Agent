"""
Application configuration.

All configurable values should live here.
"""

from state.models import Category

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


# ------------------------------
# Category Configuration
# ------------------------------

CATEGORY_KEYWORDS = {

    Category.MODEL: [
        "gpt",
        "gpt-4",
        "gpt-5",
        "gemini",
        "claude",
        "llama",
        "mistral",
        "qwen",
        "phi",
        "deepseek",
        "grok",
    ],

    Category.AGENT: [
        "agent",
        "assistant",
        "langgraph",
        "langchain",
        "crewai",
        "autogen",
        "multi-agent",
        "workflow",
    ],

    Category.RESEARCH: [
        "research",
        "paper",
        "preprint",
        "arxiv",
        "benchmark",
        "reasoning",
        "rag",
        "evaluation",
        "dataset",
        "training",
    ],

    Category.OPEN_SOURCE: [
        "github",
        "hugging face",
        "huggingface",
        "open source",
        "repository",
        "model weights",
    ],

    Category.TOOL: [
        "sdk",
        "cli",
        "tool",
        "plugin",
        "mcp",
        "api",
        "extension",
    ],

    Category.INFRASTRUCTURE: [
        "deployment",
        "serving",
        "inference",
        "gpu",
        "cloud",
        "docker",
        "kubernetes",
        "vllm",
        "onnx",
    ],

    Category.COMPANY: [
        "openai",
        "google",
        "deepmind",
        "anthropic",
        "meta",
        "microsoft",
        "xai",
    ],
}

# ------------------------------
# Summarizer Configuration
# ------------------------------

SUMMARY_MAX_ARTICLES = 30


# ------------------------------
# Gemini Configuration
# ------------------------------

GEMINI_MODEL = "gemini-2.5-flash"

GEMINI_TEMPERATURE = 0.2

GEMINI_MAX_OUTPUT_TOKENS = 512

GEMINI_TIMEOUT = 30

GEMINI_MAX_RETRIES = 3


# ------------------------------
# Groq Configuration
# ------------------------------

GROQ_MODEL = "openai/gpt-oss-20b"

GROQ_TEMPERATURE = 0.2

GROQ_MAX_OUTPUT_TOKENS = 300

GROQ_MAX_RETRIES = 3

