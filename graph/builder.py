"""
Build and compile the LangGraph workflow for the AI Daily News Agent.
"""

from langgraph.graph import StateGraph

from state.news_state import NewsState
from graph.nodes import WORKFLOW_NODES
from graph.edges import register_edges

def build_graph():
    """
    Build and compile the AI Daily News workflow.

    Returns:
        Compiled Langgraph workflow
    """
    workflow = StateGraph(NewsState)

    #------ Register Workflow Nodes ----------

    for node_name, node in WORKFLOW_NODES.items():
        workflow.add_node(
            node_name,
            node,
        )

    # ----- Register Workflow Edges ----------
    register_edges(workflow)

    # Compile the workflow
    return workflow.compile()