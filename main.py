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
            execution_status=ExecutionStatus.PENDING,
        ),
    )

def main() -> None:
    """
    Build and execute the Langgraph workflow.
    """

    graph = build_graph()

    try:

        initial_state = create_initial_state()

        initial_state[
            "execution_info"
        ].execution_status = (
            ExecutionStatus.RUNNING
        )


        final_state = graph.invoke(initial_state)

        final_state[
            "execution_info"
        ].execution_status = (
            ExecutionStatus.COMPLETED
        )
    
    except Exception:

        initial_state[
            "execution_info"
        ].execution_status = (
            ExecutionStatus.FAILED
        )

        raise

    logger.info("Workflow completed successfully")
    logger.info(f"Execution ID : {final_state['execution_info'].execution_id}")
    logger.info(f"Status: {final_state['execution_info'].execution_status.value}")
    logger.info(
        "Collected Articles: %d",
        final_state[
            "execution_info"
        ].total_articles,
    )
    logger.info(f"Processed Articles : {len(final_state['processed_articles'])}")
    logger.info(f"Queries : {len(final_state['search_queries'])}")
    logger.info(
        "Summarized Articles: %d",
        sum(
            1 
            for article in final_state['processed_articles'] 
            if article.summary
        ),
    )

    newsletter = final_state.get(
        "newsletter",
    )

    if newsletter:

        logger.info(
            "Newsletter Title: %s",
            newsletter.title,
        )

        logger.info(
            "Newsletter Date: %s",
            newsletter.newsletter_date,
        )

        logger.info(
            "Newsletter Articles: %d",
            len(newsletter.articles),
        )

        logger.info(
            "Markdown Size: %d characters",
            len(newsletter.markdown_content or ""),
        )

    output_path = final_state.get(
        "output_path",
    )

    if output_path:

        logger.info(
            "Saved Newsletter : %s",
            output_path,
        )

    html_output_path = final_state.get(
        "html_output_path",
    )

    if html_output_path:

        logger.info(
            "Saved HTML Newsletter : %s",
            html_output_path,
        )

    logger.info("\n" + "=" * 60)

if __name__ == "__main__":
    main()























