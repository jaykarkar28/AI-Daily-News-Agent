"""
Register all workflow edges for the AI Daily News Agent.

This module defines how workflow nodes are connected inside the LangGraph.
Keeping edge definitions separate from graph construction keeps the builder
clean and makes future workflow expansion easier.
"""

from langgraph.graph import START, END
from langgraph.graph.state import StateGraph

from state.news_state import NewsState

def register_edges(workflow: StateGraph[NewsState]) -> None:
    """
    Register all workflow edges.
    
    Current workflow:
    
    START -> planner -> rss_collector -> github_collector -> END
    
    Args:
        workflow: LangGraph workflow instance.
    """

    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "rss_collector")
    workflow.add_edge("rss_collector", "github_collector")
    workflow.add_edge("github_collector", END)