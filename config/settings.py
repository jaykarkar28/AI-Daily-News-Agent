"""
Application configuration.

All configurable values should live here.
"""

import os

from dotenv import load_dotenv


from state.models import (
    Category,
    SourceGroup,
)

load_dotenv()

# ============================================================
# RSS CONFIGURATION
# ============================================================

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

# Maximum number of articles collected from each RSS feed.
RSS_MAX_ARTICLES_PER_FEED = 20

REQUEST_TIMEOUT = 15

USER_AGENT = "AI-Daily-News-Agent/1.0"


# ============================================================
# RSS SOURCE QUOTAS
# ============================================================

# Maximum number of articles selected from each
# individual RSS source during newsletter selection.

RSS_SOURCE_QUOTAS = {
    "OpenAI": 2,
    "Google DeepMind": 2,
    "Anthropic": 2,
}


# ============================================================
# GITHUB CONFIGURATION
# ============================================================

GITHUB_API_BASE_URL = "https://api.github.com"

GITHUB_API_VERSION = "2022-11-28"

GITHUB_REPOSITORIES_PER_QUERY = 10

GITHUB_TRUST_SCORE = 0.9


# ============================================================
# GITHUB QUALITY FILTER
# ============================================================

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


# ============================================================
# RANKING CONFIGURATION
# ============================================================

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


# ============================================================
# CATEGORY CONFIGURATION
# ============================================================

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


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_MODEL = "gemini-2.5-flash"

GEMINI_TEMPERATURE = 0.2

GEMINI_MAX_OUTPUT_TOKENS = 512

GEMINI_TIMEOUT = 30

GEMINI_MAX_RETRIES = 3


# ============================================================
# GROQ CONFIGURATION
# ============================================================

GROQ_API_KEYS = [
    os.getenv("GROQ_API_KEY_PRIMARY"),
    os.getenv("GROQ_API_KEY_BACKUP"),
]

# Remove empty keys.

GROQ_API_KEYS = [
    key
    for key in GROQ_API_KEYS
    if key
]

GROQ_MODEL = "openai/gpt-oss-20b"

GROQ_TEMPERATURE = 0.2

GROQ_MAX_OUTPUT_TOKENS = 300

# Number of attempts per key.

GROQ_MAX_RETRIES = 3


# ============================================================
# NEWSLETTER CONFIGURATION
# ============================================================

# Maximum number of articles selected
# for the final newsletter.

NEWSLETTER_TOTAL_ARTICLES = 30


# Maximum number of articles selected
# from each editorial source group.

SOURCE_GROUP_QUOTAS = {
    SourceGroup.OFFICIAL: 10,
    SourceGroup.RESEARCH: 6,
    SourceGroup.OPEN_SOURCE: 6,
    SourceGroup.AI_NEWS: 4,
    SourceGroup.COMMUNITY: 4,
}


# ============================================================
# EMAIL CONFIGURATION
# ============================================================

EMAIL_SMTP_SERVER = "smtp.gmail.com"

EMAIL_SMTP_PORT = 587

EMAIL_TIMEOUT = 30

EMAIL_SUBJECT = "🤖 AI Daily News"


# ------------------------------
# Research / arXiv Configuration
# ------------------------------

# arXiv categories used for collecting the latest
# AI and ML research papers


ARXIV_CATEGORIES = [
    "cs.AI",  # Artificial Intelligence
    "cs.LG",  # Machine Learning
    "cs.CL",  # Computation and Language
    "cs.CV",  # Computer Vision and Pattern Recognition
    "cs.NE",  # Neural and Evolutionary Computing
    "cs.RO",  # Robotics
    "stat.ML",  # Statistics - Machine Learning
]


# Maximum Number of papers requested from arXIV
# before filtering
ARXIV_MAX_RESULTS = 50

# Keep only papers published within the last N days.
ARXIV_MAX_AGE_DAYS = 7

# Maximum number of papers collected
# for a single workflow execution
ARXIV_MAX_ARTICLES = 20

# Trust score assigned to arXiv papers
ARXIV_TRUST_SCORE = 0.95

# Keywords used to identify AI/ML-related
# research papers from arXiv.

ARXIV_AI_KEYWORDS = [

    # Core AI / ML
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "neural network",
    "neural networks",

    # Large Language Models
    "llm",
    "large language model",
    "large language models",
    "language model",
    "language models",
    "gpt",
    "transformer",

    # Generative AI
    "generative ai",
    "generative model",
    "diffusion",
    "image generation",
    "text generation",

    # AI Agents
    "agent",
    "agentic",
    "multi-agent",
    "autonomous agent",
    "tool use",

    # NLP
    "natural language processing",
    "nlp",
    "language understanding",
    "text classification",

    # Computer Vision
    "computer vision",
    "image recognition",
    "object detection",
    "image segmentation",
    "vision-language",
    "multimodal",

    # Modern AI
    "retrieval-augmented generation",
    "rag",
    "reasoning",
    "foundation model",
    "foundation models",
    "fine-tuning",
    "embedding",
    "embeddings",

    # AI Research
    "benchmark",
    "inference",
    "model training",
]


# ------------------------------
# arXiv AI Relevance Scoring
# ------------------------------

# High-priority topics for the AI Daily News newsletter.
# These receive the highest relevance score.

ARXIV_HIGH_PRIORITY_KEYWORDS = [
    "large language model",
    "large language models",
    "llm",
    "llms",
    "generative ai",
    "foundation model",
    "foundation models",
    "agentic ai",
    "ai agent",
    "ai agents",
    "llm agent",
    "llm agents",
    "multi-agent",
    "reasoning",
    "chain of thought",
    "retrieval-augmented generation",
    "rag",
    "multimodal",
    "vision-language",
    "language model",
    "language models",
]


# Important modern AI topics.
# These receive a medium relevance score.

ARXIV_MEDIUM_PRIORITY_KEYWORDS = [
    "transformer",
    "generative model",
    "diffusion model",
    "diffusion models",
    "text-to-image",
    "image generation",
    "video generation",
    "tool use",
    "computer use",
    "model routing",
    "fine-tuning",
    "alignment",
    "unlearning",
    "synthetic data",
    "reinforcement learning",
    "self-improvement",
    "embodied ai",
]


# General AI/ML terms.
# These receive a lower relevance score because
# they can appear in many domain-specific papers.

ARXIV_LOW_PRIORITY_KEYWORDS = [
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "neural network",
    "neural networks",
    "benchmark",
    "inference",
    "embedding",
    "embeddings",
    "computer vision",
    "natural language processing",
    "nlp",
    "model training",
]


# Minimum total relevance score required for a paper
# to be included in the AI Daily News pipeline.

ARXIV_MIN_RELEVANCE_SCORE = 3


# Score assigned to each keyword priority level.

ARXIV_HIGH_PRIORITY_SCORE = 3
ARXIV_MEDIUM_PRIORITY_SCORE = 2
ARXIV_LOW_PRIORITY_SCORE = 1



# ------------------------------
# arXiv Domain Penalty Configuration
# ------------------------------

# Domain-specific topics that are usually less relevant
# to a general AI Daily News newsletter.
#
# These topics are not completely excluded. Instead,
# they receive a relevance penalty so that major AI
# research can rank above domain-specific applications.

ARXIV_DOMAIN_PENALTY_KEYWORDS = [
    "medical imaging",
    "clinical",
    "patient",
    "healthcare",
    "electronic health records",
    "myocardial",
    "sleep monitoring",
    "music information retrieval",
    "music retrieval",
    "travel behavior",
    "weather-sensitive",
    "radar sensing",
    "human activity monitoring",
    "industrial",
    "travel",
    "demand prediction",
    "medical report",
    "medical reports",
    "medical",
    "health",
]


# Score deducted for each matched domain-specific keyword.
ARXIV_DOMAIN_PENALTY_SCORE = 4