from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SourceType(str, Enum):
    """
    Defines where a news article was collected from.
    """

    OFFICIAL = "official"
    RSS = "rss"
    GITHUB = "github"
    HUGGINGFACE = "huggingface"
    ARXIV = "arxiv"
    WEB_SEARCH = "web_search"

class Category(str, Enum):
    """
    Defines the category of an AI news article.
    """

    MODEL_RELEASE = "Model Release"
    RESEARCH = "Research"
    OPEN_SOURCE = "Open Source"
    COMPANY_UPDATE = "Company Update"
    FUNDING = "Funding"
    HARDWARE = "Hardware"
    AI_TOOL = "AI Tool"
    ROBOTICS = "Robotics"
    POLICY = "Policy"
    SECURITY = "Security"

class Source(BaseModel):
    """
    Represents the source from which a news article was collected.
    """

    name: str = Field(
        ...,
        description="Human-readable source name (e.g., OpenAI, Github)"
    )

    url: str = Field(
        ...,
        description="Official URL of the source"
    )

    source_type: SourceType = Field(
        ...,
        description="Type of source"
    )

    is_official: bool = Field(
        default=False,
        description="Whether this is an official company source"
    )

    trust_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Source reliability score between 0 and 1"
    )

class Article(BaseModel):
    """
    Standard news article used throughout the application.
    Every collector must return this model.
    """

    id: str = Field(
        ...,
        description="Unique identifier for the article"
    )

    title: str = Field(
        ...,
        description = "News headline"
    )

    url: str= Field(
        ...,
        description="Original article URL"
    )

    source: Source = Field(
        ...,
        description=" Source information"
    )

    published_at: datetime = Field(
        ...,
        description="Publication date and time"
    )

    summary: Optional[str] = Field(
        default=None,
        description="Generate summary"
    )

    content: Optional[str] = Field(
        default=None,
        description="Full article content"
    ) 

    category: Optional[Category] = Field(
        default=None,
        description="Article category"
    )

    tags: list[str] = Field(
        default_factory=list,
        description="Keywords"
    )

    relevance_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Importance score"
    )

    trust_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Trust score inherited from source"
    )
