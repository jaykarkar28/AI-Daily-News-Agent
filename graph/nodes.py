"""
Central registry for all LangGraph nodes.

This module imports and exposes every workflow node used by the AI Daily News Agent.
Keeping node imports in one place keeps the graph builder clean and makes future expansion easier.
"""

from agents.planner import planner_node
from agents.collectors.rss import rss_collector_node
from agents.deduplicator import deduplicator_node
from agents.collectors.github import github_collector_node
from agents.ranking import ranking_node
from agents.categorizer import categorizer_node
from agents.summarizer import summarize_node
from agents.selection import selection_node
from agents.newsletter import newsletter_node
from agents.writer import writer_node
from agents.github_filter import github_filter_node
from agents.html_generator import html_generator_node
from typing import Any, Callable

# Registry of workflow nodes.
#
# Key -> Node name used inside Langgraph
# Value -> Callable implementing that node.
# 
#  Add new nodes here as the workflow grows.

WORKFLOW_NODES: dict[str, Callable[..., Any]] = {
    "planner": planner_node,
    "rss_collector": rss_collector_node,
    "github_collector": github_collector_node,
    "github_filter": github_filter_node,
    "deduplicator": deduplicator_node,
    "ranking": ranking_node,
    "categorizer": categorizer_node,
    "selection": selection_node,
    "summarizer": summarize_node,
    "newsletter": newsletter_node,
    "html_generator": html_generator_node,
    "writer": writer_node,
}
