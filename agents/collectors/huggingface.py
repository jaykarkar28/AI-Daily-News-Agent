from typing import Any

from datetime import UTC, datetime, timedelta

from huggingface_hub import HfApi

from agents.collectors.base import BaseCollector
from state.models import (
    Article,
    Source,
    SourceGroup,
    SourceType,
)
from state.news_state import NewsState
from utils.ids import generate_article_id
from utils.logger import get_logger


logger = get_logger(__name__)


# --------------------------------------------------
# AI Relevance Filtering
# --------------------------------------------------

AI_RELEVANCE_KEYWORDS = [
    "ai",
    "llm",
    "language",
    "nlp",
    "transformer",
    "bert",
    "gpt",
    "qwen",
    "llama",
    "mistral",
    "gemma",
    "deepseek",
    "reasoning",
    "agent",
    "agentic",
    "embedding",
    "reranker",
    "retrieval",
    "rag",
    "vision",
    "image",
    "video",
    "multimodal",
    "speech",
    "audio",
    "whisper",
    "voice",
    "diffusion",
    "generation",
    "generative",
    "robot",
    "robotics",
    "segmentation",
    "detection",
    "ocr",
    "machine-learning",
    "machine learning",
    "deep-learning",
    "deep learning",
    "neural",
]

NON_AI_KEYWORDS = [
    "price-alert",
    "price alert",
    "plant-care",
    "plant care",
    "reminder",
    "e-commerce",
    "ecommerce",
    "mlb-game",
    "property-price",
    "property price",
    "todo",
    "calculator",
    "weather app",
    "restaurant",
    "recipe",
    "portfolio website",
]


class HuggingFaceCollector(BaseCollector):
    """
    Collect high-quality, relevant, and recently active
    AI content from Hugging Face.

    Collection strategy:
    - Fetch recently updated items
    - Filter obvious non-AI content
    - Filter low-quality / inactive items
    - Score using recency, downloads, and likes
    - Select the highest-quality items

    Collects:
    - Models
    - Datasets
    - Spaces
    """

    HF_BASE_URL = "https://huggingface.co"

    # --------------------------------------------------
    # Recency
    # --------------------------------------------------

    MAX_AGE_DAYS = 30

    # --------------------------------------------------
    # Final limits
    # --------------------------------------------------

    MAX_MODELS = 5
    MAX_DATASETS = 5
    MAX_SPACES = 5

    # Fetch more candidates before filtering/scoring.
    FETCH_LIMIT = 100

    # --------------------------------------------------
    # Minimum quality thresholds
    # --------------------------------------------------

    MIN_MODEL_DOWNLOADS = 100
    MIN_MODEL_LIKES = 2

    MIN_DATASET_DOWNLOADS = 100
    MIN_DATASET_LIKES = 2

    MIN_SPACE_LIKES = 2

    def __init__(self) -> None:
        self.api = HfApi()

    # --------------------------------------------------
    # Main Collection
    # --------------------------------------------------

    def collect(self) -> list[Article]:
        """
        Collect high-quality, relevant, and recent
        Hugging Face content.
        """

        articles: list[Article] = []

        logger.info(
            "Starting Hugging Face hybrid trending collection."
        )

        articles.extend(
            self._collect_models()
        )

        articles.extend(
            self._collect_datasets()
        )

        articles.extend(
            self._collect_spaces()
        )

        logger.info(
            "Total Hugging Face items collected: %d",
            len(articles),
        )

        return articles

    # --------------------------------------------------
    # AI Relevance Filtering
    # --------------------------------------------------

    def _get_item_tags(
        self,
        item: Any,
    ) -> list[str]:
        """
        Safely extract tags from a Hugging Face item.
        """

        tags = getattr(
            item,
            "tags",
            None,
        )

        if not tags:
            return []

        return [
            str(tag)
            for tag in tags
        ]

    def _is_ai_relevant(
        self,
        item_id: str,
        tags: list[str] | None = None,
    ) -> bool:
        """
        Check whether a Hugging Face item appears
        relevant to AI, machine learning, or
        generative AI.

        The filter:
        1. Rejects obvious non-AI items.
        2. Accepts items with AI/ML keywords in their
           name or tags.
        """

        searchable_text = item_id.lower()

        if tags:
            searchable_text += " " + " ".join(
                str(tag).lower()
                for tag in tags
            )

        # Reject obvious non-AI content first.
        for keyword in NON_AI_KEYWORDS:

            if keyword in searchable_text:

                logger.info(
                    "Rejected non-AI Hugging Face item: %s",
                    item_id,
                )

                return False

        # Accept AI/ML-related content.
        is_relevant = any(
            keyword in searchable_text
            for keyword in AI_RELEVANCE_KEYWORDS
        )

        if not is_relevant:

            logger.info(
                "Rejected low-relevance Hugging Face item: %s",
                item_id,
            )

        return is_relevant

    # --------------------------------------------------
    # Models
    # --------------------------------------------------

    def _collect_models(self) -> list[Article]:
        """
        Collect high-quality recent AI models.
        """

        candidates: list[
            tuple[float, Any, datetime]
        ] = []

        try:

            logger.info(
                "Fetching Hugging Face model candidates."
            )

            models = self.api.list_models(
                sort="lastModified",
                limit=self.FETCH_LIMIT,
            )

            for model in models:

                # ------------------------------------------
                # AI relevance filtering
                # ------------------------------------------

                tags = self._get_item_tags(
                    model
                )

                if not self._is_ai_relevant(
                    item_id=model.id,
                    tags=tags,
                ):

                    continue

                # ------------------------------------------
                # Recency filtering
                # ------------------------------------------

                published_at = self._get_item_datetime(
                    model
                )

                if not self._is_recent(
                    published_at
                ):
                    continue

                # ------------------------------------------
                # Quality metrics
                # ------------------------------------------

                downloads = getattr(
                    model,
                    "downloads",
                    0,
                ) or 0

                likes = getattr(
                    model,
                    "likes",
                    0,
                ) or 0

                # Keep the item if it has meaningful
                # downloads OR community engagement.

                if (
                    downloads < self.MIN_MODEL_DOWNLOADS
                    and likes < self.MIN_MODEL_LIKES
                ):
                    continue

                # ------------------------------------------
                # Score candidate
                # ------------------------------------------

                score = self._calculate_score(
                    downloads=downloads,
                    likes=likes,
                    published_at=published_at,
                )

                candidates.append(
                    (
                        score,
                        model,
                        published_at,
                    )
                )

        except Exception:

            logger.exception(
                "Failed to fetch Hugging Face models."
            )

        # Sort highest quality items first.
        candidates.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        articles: list[Article] = []

        for score, model, published_at in candidates[
            :self.MAX_MODELS
        ]:

            downloads = getattr(
                model,
                "downloads",
                0,
            ) or 0

            likes = getattr(
                model,
                "likes",
                0,
            ) or 0

            articles.append(
                self._create_article(
                    title=(
                        f"Trending Model: {model.id}"
                    ),
                    url=(
                        f"{self.HF_BASE_URL}/{model.id}"
                    ),
                    summary=(
                        f"Recently active AI model on "
                        f"Hugging Face with {likes} likes "
                        f"and {downloads} downloads."
                    ),
                    published_at=published_at,
                )
            )

            logger.info(
                "Selected model: %s | Score: %.2f",
                model.id,
                score,
            )

        logger.info(
            "Collected %d high-quality Hugging Face models.",
            len(articles),
        )

        return articles

    # --------------------------------------------------
    # Datasets
    # --------------------------------------------------

    def _collect_datasets(self) -> list[Article]:
        """
        Collect high-quality recent AI datasets.
        """

        candidates: list[
            tuple[float, Any, datetime]
        ] = []

        try:

            logger.info(
                "Fetching Hugging Face dataset candidates."
            )

            datasets = self.api.list_datasets(
                sort="lastModified",
                limit=self.FETCH_LIMIT,
            )

            for dataset in datasets:

                # ------------------------------------------
                # AI relevance filtering
                # ------------------------------------------

                tags = self._get_item_tags(
                    dataset
                )

                if not self._is_ai_relevant(
                    item_id=dataset.id,
                    tags=tags,
                ):

                    continue

                # ------------------------------------------
                # Recency filtering
                # ------------------------------------------

                published_at = self._get_item_datetime(
                    dataset
                )

                if not self._is_recent(
                    published_at
                ):
                    continue

                # ------------------------------------------
                # Quality metrics
                # ------------------------------------------

                downloads = getattr(
                    dataset,
                    "downloads",
                    0,
                ) or 0

                likes = getattr(
                    dataset,
                    "likes",
                    0,
                ) or 0

                if (
                    downloads < self.MIN_DATASET_DOWNLOADS
                    and likes < self.MIN_DATASET_LIKES
                ):
                    continue

                # ------------------------------------------
                # Score candidate
                # ------------------------------------------

                score = self._calculate_score(
                    downloads=downloads,
                    likes=likes,
                    published_at=published_at,
                )

                candidates.append(
                    (
                        score,
                        dataset,
                        published_at,
                    )
                )

        except Exception:

            logger.exception(
                "Failed to fetch Hugging Face datasets."
            )

        candidates.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        articles: list[Article] = []

        for score, dataset, published_at in candidates[
            :self.MAX_DATASETS
        ]:

            downloads = getattr(
                dataset,
                "downloads",
                0,
            ) or 0

            likes = getattr(
                dataset,
                "likes",
                0,
            ) or 0

            articles.append(
                self._create_article(
                    title=(
                        f"Trending Dataset: {dataset.id}"
                    ),
                    url=(
                        f"{self.HF_BASE_URL}/datasets/"
                        f"{dataset.id}"
                    ),
                    summary=(
                        f"Recently active AI dataset on "
                        f"Hugging Face with {likes} likes "
                        f"and {downloads} downloads."
                    ),
                    published_at=published_at,
                )
            )

            logger.info(
                "Selected dataset: %s | Score: %.2f",
                dataset.id,
                score,
            )

        logger.info(
            "Collected %d high-quality Hugging Face datasets.",
            len(articles),
        )

        return articles

    # --------------------------------------------------
    # Spaces
    # --------------------------------------------------

    def _collect_spaces(self) -> list[Article]:
        """
        Collect high-quality recent AI Spaces.
        """

        candidates: list[
            tuple[float, Any, datetime]
        ] = []

        try:

            logger.info(
                "Fetching Hugging Face Space candidates."
            )

            spaces = self.api.list_spaces(
                sort="lastModified",
                limit=self.FETCH_LIMIT,
            )

            for space in spaces:

                # ------------------------------------------
                # AI relevance filtering
                # ------------------------------------------

                tags = self._get_item_tags(
                    space
                )

                if not self._is_ai_relevant(
                    item_id=space.id,
                    tags=tags,
                ):

                    continue

                # ------------------------------------------
                # Recency filtering
                # ------------------------------------------

                published_at = self._get_item_datetime(
                    space
                )

                if not self._is_recent(
                    published_at
                ):
                    continue

                # ------------------------------------------
                # Quality metrics
                # ------------------------------------------

                likes = getattr(
                    space,
                    "likes",
                    0,
                ) or 0

                if likes < self.MIN_SPACE_LIKES:
                    continue

                # Spaces do not always provide useful
                # download counts, so score using likes
                # and recency.

                score = self._calculate_score(
                    downloads=0,
                    likes=likes,
                    published_at=published_at,
                )

                candidates.append(
                    (
                        score,
                        space,
                        published_at,
                    )
                )

        except Exception:

            logger.exception(
                "Failed to fetch Hugging Face Spaces."
            )

        candidates.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        articles: list[Article] = []

        for score, space, published_at in candidates[
            :self.MAX_SPACES
        ]:

            likes = getattr(
                space,
                "likes",
                0,
            ) or 0

            articles.append(
                self._create_article(
                    title=(
                        f"Trending Space: {space.id}"
                    ),
                    url=(
                        f"{self.HF_BASE_URL}/spaces/"
                        f"{space.id}"
                    ),
                    summary=(
                        f"Recently active AI Space on "
                        f"Hugging Face with {likes} likes."
                    ),
                    published_at=published_at,
                )
            )

            logger.info(
                "Selected Space: %s | Score: %.2f",
                space.id,
                score,
            )

        logger.info(
            "Collected %d high-quality Hugging Face Spaces.",
            len(articles),
        )

        return articles

    # --------------------------------------------------
    # Scoring
    # --------------------------------------------------

    def _calculate_score(
        self,
        downloads: int,
        likes: int,
        published_at: datetime,
    ) -> float:
        """
        Calculate a hybrid trending score.

        Score components:
        - Downloads: popularity
        - Likes: community interest
        - Recency: recently updated items receive
          additional value
        """

        age = datetime.now(UTC) - published_at

        age_days = max(
            age.total_seconds() / 86400,
            0,
        )

        recency_score = max(
            self.MAX_AGE_DAYS - age_days,
            0,
        )

        # Downloads are scaled so extremely large
        # numbers do not dominate the score.

        download_score = min(
            downloads / 1000,
            100,
        )

        # Likes are a direct signal of
        # community interest.

        like_score = likes * 5

        return (
            download_score
            + like_score
            + recency_score
        )

    # --------------------------------------------------
    # Date Handling
    # --------------------------------------------------

    def _get_item_datetime(
        self,
        item: Any,
    ) -> datetime:
        """
        Extract the item's last modified datetime.
        """

        last_modified = getattr(
            item,
            "last_modified",
            None,
        )

        if last_modified is None:
            return datetime.now(UTC)

        if last_modified.tzinfo is None:
            return last_modified.replace(
                tzinfo=UTC,
            )

        return last_modified.astimezone(
            UTC,
        )

    def _is_recent(
        self,
        published_at: datetime,
    ) -> bool:
        """
        Check whether an item is within the allowed
        recent time window.
        """

        cutoff_date = (
            datetime.now(UTC)
            - timedelta(
                days=self.MAX_AGE_DAYS,
            )
        )

        return published_at >= cutoff_date

    # --------------------------------------------------
    # Article Conversion
    # --------------------------------------------------

    def _create_article(
        self,
        title: str,
        url: str,
        summary: str,
        published_at: datetime,
    ) -> Article:
        """
        Convert a Hugging Face item into the standard
        Article model.
        """

        source = Source(
            name="Hugging Face Trending",
            url=self.HF_BASE_URL,
            source_type=SourceType.HUGGINGFACE,
            group=SourceGroup.COMMUNITY,
            is_official=True,
            trust_score=0.90,
        )

        return Article(
            id=generate_article_id(url),
            title=title,
            url=url,
            source=source,
            summary=summary,
            published_at=published_at,
            trust_score=0.90,
        )


# --------------------------------------------------
# LangGraph Node
# --------------------------------------------------

def huggingface_collector_node(
    state: NewsState,
) -> dict[str, Any]:
    """
    LangGraph node for the Hugging Face Collector.
    """

    collector = HuggingFaceCollector()

    articles = collector.collect()

    logger.info(
        "Hugging Face Collector node collected %d articles.",
        len(articles),
    )

    return {
        "articles": articles,
    }