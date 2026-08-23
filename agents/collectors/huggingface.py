from typing import Any

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
from datetime import UTC, datetime

logger = get_logger(__name__)

class HuggingFaceCollector(BaseCollector):
    """
    Collect trending AI content from Hugging Face.
    
    Collects:
    - Popular models
    - Popular datasets
    - Popular spaces
    """
    
    HF_BASE_URL = "https://huggingface.co"
    
    def __init__(self) -> None:
        self.api = HfApi()
        
    def collect(self) -> list[Article]:
        """
        Collect trending Hugging Face models, datasets, and Spaces.
        """
        
        articles: list[Article] = []
        
        logger.info(
            "Starting Hugging Face trending collection."
        )
        
        articles.extend(self._collect_models())
        articles.extend(self._collect_datasets())
        articles.extend(self._collect_spaces())
        
        logger.info(
            "Total Hugging Face trending items collected: %d",
            len(articles),
        )
        
        return articles
    
    # --------------------------------------------------
    # Models
    # ------------------------------------------------
    
    def _collect_models(self) -> list[Article]:
        """
        Collect popular Hugging Face models.
        """
        
        articles: list[Article] = []
        
        try:
            logger.info(
                "Collecting Hugging Face trending models."
            )
            
            models = self.api.list_models(
                sort="downloads",
                limit=10,
            )
            
            for model in models:
                article = self._create_article(
                    item_id=model.id,
                    title=f"Trending Model: {model.id}",
                    url=f"{self.HF_BASE_URL}/{model.id}",
                    summary=(
                        f"Popular Hugging Face model with "
                        f"{getattr(model, 'downloads', 0)} downloads."
                    ),
                    content_type="model",
                )
                
                articles.append(article)
        
        except Exception:
            logger.exception(
                "Failed to collect Hugging Face models."
            )
            
        logger.info(
            "Collected %d Hugging Face models.",
            len(articles)
        )
        
        return articles
    
    # --------------------------------------------------
    # Datasets
    # --------------------------------------------------
    
    def _collect_datasets(self) -> list[Article]:
        """
        Collect popular Hugging Face datasets.
        """
        
        articles: list[Article] = []
        
        try:
            logger.info(
                "Collecting Hugging Face trending datasets."
            )
            
            datasets = self.api.list_datasets(
                sort="downloads",
                limit=10,
            )
            
            for dataset in datasets:
                article = self._create_article(
                    item_id=dataset.id,
                    title=f"Trending Dataset: {dataset.id}",
                    url=f"{self.HF_BASE_URL}/datasets/{dataset.id}",
                    summary=(
                        f"Popular Hugging Face dataset with "
                        f"{getattr(dataset, 'downloads', 0)} downloads."
                    ),
                    content_type="dataset",
                )
                
                articles.append(article)
        
        except Exception:
            logger.exception(
                "Failed to collect Hugging Face datasets."
            )
        
        logger.info(
            "Collected %d Hugging Face datasets.",
            len(articles)
        )
        
        return articles
    
    def _collect_spaces(self) -> list[Article]:
        """
        Collect popular Hugging Face Spaces.
        """
        
        articles: list[Article] = []
        
        try:
            logger.info(
                "Collecting Hugging Face trending Spaces."
            )
            
            spaces = self.api.list_spaces(
                limit=10,
            )
            
            for space in spaces:
                article = self._create_article(
                    item_id=space.id,
                    title=f"Trending Space: {space.id}",
                    url=f"{self.HF_BASE_URL}/spaces/{space.id}",
                    summary=(
                        "Popular Hugging Face Space."
                    ),
                    content_type="space",
                )
                
                articles.append(article)
        
        except Exception:
            logger.exception(
                "Failed to collect Hugging Face Spaces."
            )
        
        logger.info(
            "Collected %d Hugging Face Spaces.",
            len(articles)
        )
        
        return articles
    
    # --------------------------------------------------
    # Article Conversion
    # --------------------------------------------------    
    
    def _create_article(
        self,
        item_id: str,
        title: str,
        url: str,
        summary: str,
        content_type: str,
    ) -> Article:
        """
        Convert a Hugging Face item into the standard Article model.
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
            published_at=datetime.now(UTC),
            trust_score=0.90,
        )
        
        
        
# --------------------------------------------------
# Langgraph Node
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
        
        
        
        
        
    