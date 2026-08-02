"""
Application configuration.

All configurable values should live here.
"""

from state.models import (
    Category,
    SourceGroup,
)

import os

# ------------------------------
# RSS CONFIGURATION
# ------------------------------
RSS_FEEDS = [
    {
        "name": "OpenAI",
        "url": "https://openai.com/news/rss.xml",
        "group": SourceGroup.OFFICIAL,
        "trust_score": 1.0,
        "is_official": True,
    },
    {
        "name": "Google DeepMind",
        "url": "https://blog.google/technology/ai/rss/",
        "group": SourceGroup.OFFICIAL,
        "trust_score": 0.95,
        "is_official": True,
    },
    {
        "name": "Hugging Face",
        "url": "https://huggingface.co/blog/feed.xml",
        "group": SourceGroup.OPEN_SOURCE,
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
# GitHub Quality Filter
# ------------------------------

# Minimum score required for a GitHub repository
# to be considered AI-related.
GITHUB_MIN_AI_SCORE = 8


# AI-related keywords used while scoring repositories.
GITHUB_AI_KEYWORDS = [

    # Core AI
    "ai",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "neural network",

    # LLM
    "llm",
    "gpt",
    "gemini",
    "claude",
    "llama",
    "mistral",
    "qwen",
    "deepseek",

    # Agentic AI
    "agent",
    "agentic",
    "langgraph",
    "langchain",
    "crewai",
    "autogen",

    # RAG
    "rag",
    "retrieval",
    "embedding",
    "vector",
    "vectordb",
    "faiss",
    "chroma",
    "pinecone",

    # AI Concepts
    "reasoning",
    "prompt",
    "prompt engineering",
    "transformer",
    "attention",
    "multimodal",
    "vision",
    "ocr",
    "speech",
    "inference",
    "fine-tuning",
]


# Trusted GitHub organizations.
# Repositories from these owners receive
# additional score.
GITHUB_TRUSTED_OWNERS = [

    "openai",
    "langchain-ai",
    "huggingface",
    "microsoft",
    "google",
    "google-deepmind",
    "meta-llama",
    "mistralai",
    "vllm-project",
    "crewAIInc",
]


# Keywords that indicate the repository
# is probably NOT AI-related.
GITHUB_BLACKLIST_KEYWORDS = [

    "crypto",
    "bitcoin",
    "ethereum",

    "war",
    "iran",

    "movie",
    "music",
    "anime",

    "football",
    "soccer",

    "game",
    "gaming",

    "weather",
    "ecommerce",
]


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

GROQ_API_KEYS = [
    os.getenv("GROQ_API_KEY_PRIMARY"),
    os.getenv("GROQ_API_KEY_BACKUP"),
]

# Remove empty keys
GROQ_API_KEYS = [
    key
    for key in GROQ_API_KEYS
    if key
]

GROQ_MODEL = "openai/gpt-oss-20b"

GROQ_TEMPERATURE = 0.2

GROQ_MAX_OUTPUT_TOKENS = 300

# Number of attempts per key
GROQ_MAX_RETRIES = 3

# ------------------------------
# Newsletter Configuration
# ------------------------------

# Maximum number of articles selected
# from each editorial source group.

NEWSLETTER_TOTAL_ARTICLES = 30

SOURCE_GROUP_QUOTAS = {
    SourceGroup.OFFICIAL: 10,
    SourceGroup.RESEARCH: 6,
    SourceGroup.OPEN_SOURCE: 6,
    SourceGroup.AI_NEWS: 4,
    SourceGroup.COMMUNITY: 4,
}