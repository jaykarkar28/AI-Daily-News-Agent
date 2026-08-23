"""
Central registry for all LangGraph nodes.

This module imports and exposes every workflow node used by
the AI Daily News Agent.

Keeping node imports in one place keeps the graph builder clean
and makes future expansion easier.
"""

from typing import Any, Callable

from agents.planner import planner_node

# Collectors
from agents.collectors.rss import rss_collector_node
from agents.collectors.anthropic import anthropic_collector_node
from agents.collectors.github import github_collector_node
from agents.collectors.arxiv import arxiv_collector_node
from agents.collectors.ai_news import ai_news_collector_node
from agents.collectors.huggingface import huggingface_collector_node

# Processing Agents
from agents.deduplicator import deduplicator_node
from agents.github_filter import github_filter_node
from agents.ranking import ranking_node
from agents.categorizer import categorizer_node
from agents.selection import selection_node

# Generation Agents
from agents.summarizer import summarize_node
from agents.newsletter import newsletter_node
from agents.html_generator import html_generator_node
from agents.writer import writer_node
from agents.email_sender import email_sender_node


# Registry of workflow nodes.
#
# Key:
#     Node name used inside LangGraph.
#
# Value:
#     Callable implementing that node.
#
# Add new nodes here as the workflow grows.

WORKFLOW_NODES: dict[str, Callable[..., Any]] = {
    # Planning
    "planner": planner_node,

    # Collectors
    "rss_collector": rss_collector_node,
    "anthropic_collector": anthropic_collector_node,
    "github_collector": github_collector_node,
    "arxiv_collector": arxiv_collector_node,
    "ai_news_collector": ai_news_collector_node,
    "huggingface_collector": huggingface_collector_node,
    
    # Processing
    "deduplicator": deduplicator_node,
    "github_filter": github_filter_node,
    "ranking": ranking_node,
    "categorizer": categorizer_node,
    "selection": selection_node,

    # Content Generation
    "summarizer": summarize_node,
    "newsletter": newsletter_node,
    "html_generator": html_generator_node,
    "writer": writer_node,
    "email_sender": email_sender_node,
}