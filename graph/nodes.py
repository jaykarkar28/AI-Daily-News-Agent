"""
Central registry for all LangGraph nodes.

This module imports and exposes every workflow node used by the AI Daily News Agent.
Keeping node imports in one place keeps the graph builder clean and makes future expansion easier.
"""

from agents.planner import planner_node
from agents.collectors.rss import rss_collector_node
from agents.deduplicator import deduplicator_node
from agents.collectors.github import github_collector_node
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
    "deduplicator": deduplicator_node,
}
