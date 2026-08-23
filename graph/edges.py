"""
Register all workflow edges for the AI Daily News Agent.

This module defines how workflow nodes are connected inside LangGraph.

Collectors run in parallel after the planner and converge at the
deduplicator node.
"""

from langgraph.graph import START, END
from langgraph.graph.state import StateGraph

from state.news_state import NewsState


def register_edges(
    workflow: StateGraph[NewsState],
) -> None:
    """
    Register all workflow edges.

    Workflow:

        START
          ↓
        planner
          ↓
    ┌─────┼──────────┬───────────────────┐
    ↓     ↓          ↓                   ↓
    RSS  Anthropic  GitHub             arXiv
    │     │          │                   │
    └─────┴──────────┴─────────┬─────────┘
                               ↓
                         deduplicator
                               ↓
                          github_filter
                               ↓
                            ranking
                               ↓
                          categorizer
                               ↓
                           selection
                               ↓
                          summarizer
                               ↓
                          newsletter
                               ↓
                         html_generator
                               ↓
                            writer
                               ↓
                         email_sender
                               ↓
                              END

    Args:
        workflow:
            LangGraph StateGraph instance.
    """

    # --------------------------------------------------
    # Start
    # --------------------------------------------------

    workflow.add_edge(
        START,
        "planner",
    )

    # --------------------------------------------------
    # Planner → Parallel Collectors
    # --------------------------------------------------

    workflow.add_edge(
        "planner",
        "rss_collector",
    )

    workflow.add_edge(
        "planner",
        "anthropic_collector",
    )

    workflow.add_edge(
        "planner",
        "github_collector",
    )

    workflow.add_edge(
        "planner",
        "arxiv_collector",
    )
    
    workflow.add_edge(
        "planner",
        "ai_news_collector",
    )
    
    workflow.add_edge(
        "planner",
        "huggingface_collector",
    )
    
    workflow.add_edge(
        "planner",
        "web_search_collector",
    )

    # --------------------------------------------------
    # Parallel Collectors → Deduplicator
    # --------------------------------------------------

    workflow.add_edge(
        "rss_collector",
        "deduplicator",
    )

    workflow.add_edge(
        "anthropic_collector",
        "deduplicator",
    )

    workflow.add_edge(
        "github_collector",
        "deduplicator",
    )

    workflow.add_edge(
        "arxiv_collector",
        "deduplicator",
    )
    
    workflow.add_edge(
        "ai_news_collector",
        "deduplicator",
    )
    
    workflow.add_edge(
        "huggingface_collector",
        "deduplicator",
    )
    
    workflow.add_edge(
        "web_search_collector",
        "deduplicator",
    )

    # --------------------------------------------------
    # Main Processing Pipeline
    # --------------------------------------------------

    workflow.add_edge(
        "deduplicator",
        "github_filter",
    )

    workflow.add_edge(
        "github_filter",
        "ranking",
    )

    workflow.add_edge(
        "ranking",
        "categorizer",
    )

    workflow.add_edge(
        "categorizer",
        "selection",
    )

    workflow.add_edge(
        "selection",
        "summarizer",
    )

    workflow.add_edge(
        "summarizer",
        "newsletter",
    )

    # --------------------------------------------------
    # Newsletter Generation
    # --------------------------------------------------

    workflow.add_edge(
        "newsletter",
        "html_generator",
    )

    workflow.add_edge(
        "html_generator",
        "writer",
    )

    # --------------------------------------------------
    # Email
    # --------------------------------------------------

    workflow.add_edge(
        "writer",
        "email_sender",
    )

    workflow.add_edge(
        "email_sender",
        END,
    )