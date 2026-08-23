"""
FastAPI application for the AI Daily News Agent.
"""

from contextlib import asynccontextmanager
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool

from graph.builder import build_graph
from state.models import ExecutionInfo, ExecutionStatus
from state.news_state import NewsState
from utils.logger import get_logger, setup_logging


load_dotenv()
setup_logging()

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Build the LangGraph workflow once when
    the FastAPI application starts.
    """

    logger.info("Starting FastAPI application.")

    app.state.graph = build_graph()

    logger.info("LangGraph workflow loaded successfully.")

    yield

    logger.info("Shutting down FastAPI application.")


app = FastAPI(
    title="AI Daily News Agent API",
    description=(
        "API for generating daily AI news using "
        "a multi-agent LangGraph workflow."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


def create_initial_state() -> NewsState:
    """
    Create the initial workflow state.
    """

    return NewsState(
        execution_info=ExecutionInfo(
            execution_id=str(uuid4()),
            execution_status=ExecutionStatus.PENDING,
        ),
    )


@app.get("/")
def root() -> dict:
    """
    Root API endpoint.
    """

    return {
        "message": "AI Daily News Agent API is running.",
        "docs": "/docs",
    }


@app.get("/health")
def health_check() -> dict:
    """
    Check whether the API is running.
    """

    return {
        "status": "healthy",
        "service": "AI Daily News Agent",
    }


@app.post("/news/generate")
async def generate_news() -> dict:
    """
    Execute the complete AI Daily News workflow.

    Returns generated newsletter information,
    output file paths, and execution details.
    """

    logger.info("API request received to generate AI news.")

    initial_state = create_initial_state()

    initial_state[
        "execution_info"
    ].execution_status = ExecutionStatus.RUNNING

    try:

        graph = app.state.graph

        final_state = await run_in_threadpool(
            graph.invoke,
            initial_state,
        )

        final_state[
            "execution_info"
        ].execution_status = (
            ExecutionStatus.COMPLETED
        )

    except Exception as error:

        logger.exception(
            "AI news workflow failed."
        )

        initial_state[
            "execution_info"
        ].execution_status = (
            ExecutionStatus.FAILED
        )

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )

    execution_info = final_state.get(
        "execution_info",
    )

    newsletter = final_state.get(
        "newsletter",
    )

    processed_articles = final_state.get(
        "processed_articles",
        [],
    )

    logger.info(
        "API workflow completed successfully."
    )

    return {
        "success": True,
        "execution_id": (
            execution_info.execution_id
            if execution_info
            else None
        ),
        "status": (
            execution_info.execution_status.value
            if execution_info
            else "completed"
        ),
        "collected_articles": (
            execution_info.total_articles
            if execution_info
            else 0
        ),
        "processed_articles": len(
            processed_articles
        ),
        "newsletter": {
            "title": (
                newsletter.title
                if newsletter
                else None
            ),
            "date": (
                str(newsletter.newsletter_date)
                if newsletter
                else None
            ),
            "article_count": (
                len(newsletter.articles)
                if newsletter
                else 0
            ),
            "markdown_content": (
                newsletter.markdown_content
                if newsletter
                else None
            ),
        },
        "output_path": final_state.get(
            "output_path",
        ),
        "html_output_path": final_state.get(
            "html_output_path",
        ),
        "email_sent": final_state.get(
            "email_sent",
        ),
    }