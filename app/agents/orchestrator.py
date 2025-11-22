"""
Agent orchestrator - coordinates the research graph generation pipeline.
"""
import time
from datetime import datetime
from typing import Optional
from app.agents.models import AgentContext, ExtractedFilters
from app.agents.intent_agent import IntentExtractionAgent
from app.agents.search_agent import SearchAgent
from app.agents.extraction_agent import ExtractionAgent
from app.services.state_manager import state_manager
from app.utils.paper_mapper import get_preview_papers


class ResearchAgentOrchestrator:
    """
    Orchestrates the entire research graph generation process.

    Pipeline:
    1. Intent & Filter Extraction
    2. OpenAlex Search
    3. Data Extraction (TODO)
    4. Relationship Building (TODO)
    5. Graph Construction (TODO)
    """

    def __init__(self):
        self.intent_agent = IntentExtractionAgent()
        self.search_agent = SearchAgent()
        self.extraction_agent = ExtractionAgent()

    def run(self, context: AgentContext) -> None:
        """
        Execute the full research pipeline.

        This method runs the entire process and updates the state manager
        with step-by-step progress.

        Args:
            context: Agent execution context with run_id, query, cv_id, etc.
        """
        run_id = context.run_id

        try:
            # Step 1: Intent & Filter Extraction
            self._execute_intent_extraction(context)

            # Step 2: OpenAlex Search
            self._execute_search(context)

            # Step 3: Data Extraction
            self._execute_extraction(context)

            # TODO: Add remaining steps
            # Step 4: Relationship Building
            # Step 5: Graph Construction

            # For now, add placeholder for remaining steps
            self._add_placeholder_steps(context)

            # Mark as completed
            state_manager.update_run_status(run_id, "completed")

        except Exception as e:
            # Log error and mark as failed
            self._log_error(run_id, str(e))
            state_manager.update_run_status(run_id, "completed")  # Still mark as completed for now

    def _execute_intent_extraction(self, context: AgentContext) -> None:
        """
        Step 1: Extract intent and filters from query and CV.
        """
        run_id = context.run_id

        # Add initial "intent" step (in_progress)
        state_manager.add_run_step(
            run_id=run_id,
            step_id="intent-1",
            step_type="intent",
            message="Understanding user intentions...",
            details=None,
            sources=[],
            status="in_progress"
        )

        time.sleep(1)  # Simulate thinking

        try:
            # Extract filters using the agent
            filters = self.intent_agent.extract_with_context(context)

            # Store filters in context
            context.filters = filters

            # Update the step to "done" with extracted filters
            state_manager.add_run_step(
                run_id=run_id,
                step_id="filters-1",
                step_type="filters",
                message="Extracted research filters",
                filters={
                    "topics": filters.topics,
                    "geographical_areas": filters.geographical_areas
                },
                status="done"
            )

        except Exception as e:
            # Mark intent as done with error
            state_manager.add_run_step(
                run_id=run_id,
                step_id="filters-1",
                step_type="filters",
                message=f"Failed to extract filters: {str(e)}",
                status="done"
            )
            raise

    def _execute_search(self, context: AgentContext) -> None:
        """
        Step 2: Search for papers using OpenAlex API.
        """
        run_id = context.run_id

        # Add initial "search" step (in_progress)
        state_manager.add_run_step(
            run_id=run_id,
            step_id="search-1",
            step_type="search",
            message="Looking for relevant papers associated to your research...",
            status="in_progress"
        )

        time.sleep(1)  # Brief pause for UX

        try:
            # Search papers using the agent (fetches 2 * max_nodes)
            search_results = self.search_agent.search_papers(context)
            papers_data = search_results.get("results", [])

            # Store full papers data in context for later processing (extraction step)
            context.papers_data = papers_data

            # Map first 4 papers to Paper objects for frontend display
            preview_papers = get_preview_papers(papers_data, limit=4)

            # Convert Paper objects to dict for JSON serialization
            preview_papers_dict = [paper.model_dump() for paper in preview_papers]

            # Update the step to "done" with preview papers
            state_manager.add_run_step(
                run_id=run_id,
                step_id="search-1",
                step_type="search",
                message=f"Found {len(papers_data)} relevant papers",
                papers=preview_papers_dict,  # Only first 4 papers for frontend
                status="done"
            )

        except Exception as e:
            # Mark search as done with error
            state_manager.add_run_step(
                run_id=run_id,
                step_id="search-1",
                step_type="search",
                message=f"Failed to search papers: {str(e)}",
                status="done"
            )
            raise

    def _execute_extraction(self, context: AgentContext) -> None:
        """
        Step 3: Extract professors from papers.
        """
        run_id = context.run_id

        # Add initial "extraction" step (in_progress)
        state_manager.add_run_step(
            run_id=run_id,
            step_id="extraction-1",
            step_type="extraction",
            message="Extracting professors from papers...",
            status="in_progress"
        )

        time.sleep(1)  # Brief pause for UX

        try:
            # Extract professors using the agent
            professor_nodes, basic_professors = self.extraction_agent.extract_professors(context)

            # Store full professor nodes in context for final graph construction
            context.professor_nodes = [node.model_dump() for node in professor_nodes]

            # Convert BasicProfessor objects to dict for JSON serialization
            basic_professors_dict = [prof.model_dump() for prof in basic_professors]

            # Update the step to "done" with basic professors for display
            state_manager.add_run_step(
                run_id=run_id,
                step_id="extraction-1",
                step_type="extraction",
                message=f"Extracted {len(basic_professors)} professors",
                professors=basic_professors_dict,  # For frontend display
                status="done"
            )

        except Exception as e:
            # Mark extraction as done with error
            state_manager.add_run_step(
                run_id=run_id,
                step_id="extraction-1",
                step_type="extraction",
                message=f"Failed to extract professors: {str(e)}",
                status="done"
            )
            raise

    def _add_placeholder_steps(self, context: AgentContext) -> None:
        """Add placeholder steps for remaining pipeline stages."""
        run_id = context.run_id

        # Relationships step
        time.sleep(1)
        state_manager.add_run_step(
            run_id=run_id,
            step_id="relationships-1",
            step_type="relationships",
            message="Building relationship graph...",
            details=None,
            sources=[],
            status="done"
        )

        # Graph construction step
        time.sleep(1)
        state_manager.add_run_step(
            run_id=run_id,
            step_id="graph-1",
            step_type="graph",
            message="Constructing 3D graph visualization...",
            details={"node_count": context.max_nodes},
            sources=[],
            status="done"
        )

        # Add mock graph data
        from app.services.simulation_service import generate_mock_graph
        graph_data = generate_mock_graph(context.max_nodes)
        state_manager.set_run_graph(run_id, graph_data)

    def _log_error(self, run_id: str, error_message: str) -> None:
        """Log error to state manager."""
        state_manager.add_run_step(
            run_id=run_id,
            step_id=f"error-{datetime.utcnow().timestamp()}",
            step_type="intent",
            message=f"Error: {error_message}",
            details=None,
            sources=[],
            status="done"
        )
