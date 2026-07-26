"""
Entry point for the AI daily news agent.
"""

from graph.builder import build_graph
from state.news_state import NewsState
from state.models import ExecutionInfo, ExecutionStatus
from uuid import uuid4

from utils.logger import get_logger, setup_logging
from dotenv import load_dotenv

load_dotenv()
setup_logging()

logger = get_logger(__name__)


logger.info("Workflow started.")

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

    
    logger.info("Workflow completed successfully")
    logger.info(f"Execution ID : {final_state['execution_info'].execution_id}")
    logger.info(f"Status       : {final_state['execution_info'].execution_status.value}")
    logger.info(f"Articles     : {len(final_state['articles'])}")
    logger.info(f"Queries      : {len(final_state['search_queries'])}")
    logger.info("\n" + "=" * 60)

if __name__ == "__main__":
    main()