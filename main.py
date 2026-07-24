"""
Entry point for the AI daily news agent.
"""

from graph.builder import build_graph
from state.news_state import NewsState
from state.models import ExecutionInfo, ExecutionStatus
from uuid import uuid4

from dotenv import load_dotenv

load_dotenv()

import os
print(f"Loaded GITHUB_API_TOKEN: {os.getenv('GITHUB_API_TOKEN')}")

def create_initial_state() -> NewsState:
    """
    Create the initial workflow state
    
    Returns:
        initialized NewsState
    """

    return NewsState(
        execution_info=ExecutionInfo(
            execution_id=str(uuid4()),
            status=ExecutionStatus.PENDING,
        ),
    )

def main() -> None:
    """
    Build and execute the Langgraph workflow.
    """

    graph = build_graph()

    initial_state = create_initial_state()

    final_state = graph.invoke(initial_state)

    print("\n" + "=" * 60)
    print("Workflow completed successfully")
    print("=" * 60)

    print(f"Execution ID : {final_state['execution_info'].execution_id}")
    print(f"Status       : {final_state['execution_info'].execution_status.value}")
    print(f"Articles     : {len(final_state['articles'])}")
    print(f"Queries      : {len(final_state['search_queries'])}")


if __name__ == "__main__":
    main()