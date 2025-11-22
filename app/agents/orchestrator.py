"""
Agent orchestrator - coordinates the research graph generation pipeline.
"""
import time
from datetime import datetime
from typing import Optional
from app.agents.models import AgentContext, ExtractedFilters
from app.agents.intent_agent import IntentExtractionAgent
from app.services.state_manager import state_manager


class ResearchAgentOrchestrator:
    """
    Orchestrates the entire research graph generation process.

    Pipeline:
    1. Intent & Filter Extraction
    2. OpenAlex Search (TODO)
    3. Data Extraction (TODO)
    4. Relationship Building (TODO)
    5. Graph Construction (TODO)
    """

    def __init__(self):
        self.intent_agent = IntentExtractionAgent()

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

            # TODO: Add remaining steps
            # Step 2: OpenAlex Search
            # Step 3: Data Extraction
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
                details={
                    "topics": filters.topics,
                    "geographical_areas": filters.geographical_areas
                },
                sources=[],
                status="done"
            )

        except Exception as e:
            # Mark intent as done with error
            state_manager.add_run_step(
                run_id=run_id,
                step_id="filters-1",
                step_type="filters",
                message=f"Failed to extract filters: {str(e)}",
                details=None,
                sources=[],
                status="done"
            )
            raise

    def _add_placeholder_steps(self, context: AgentContext) -> None:
        """Add placeholder steps for remaining pipeline stages."""
        run_id = context.run_id

        # Search step
        time.sleep(1)
        state_manager.add_run_step(
            run_id=run_id,
            step_id="search-1",
            step_type="search",
            message="Searching OpenAlex for relevant research...",
            details={"query_count": context.max_nodes},
            sources=[],
            status="done"
        )

        # Extraction step
        time.sleep(1)
        state_manager.add_run_step(
            run_id=run_id,
            step_id="extraction-1",
            step_type="extraction",
            message="Extracting entities and relationships...",
            details=None,
            sources=[],
            status="done"
        )

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
