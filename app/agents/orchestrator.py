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
from app.database.database import db
from app.utils.paper_mapper import get_preview_papers
from app.utils.graph_builder import build_graph_links, create_user_node
from app.schemas.agent import GraphData, GraphNode


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

            # Step 4: Relationship Building
            self._execute_relationships(context)

            # Step 5: Graph Construction
            self._execute_graph_construction(context)

            # Mark as completed
            state_manager.update_run_status(run_id, "completed")

            # Save to database
            self._save_run_to_database(context)

        except Exception as e:
            # Log error and mark as failed
            self._log_error(run_id, str(e))
            state_manager.update_run_status(run_id, "completed")  # Still mark as completed for now

            # Still try to save to database (even if there was an error)
            self._save_run_to_database(context)

    def _execute_intent_extraction(self, context: AgentContext) -> None:
        """
        Step 1: Extract intent and filters from query and CV.
        """
        run_id = context.run_id

        try:
            # Extract filters using the agent
            filters = self.intent_agent.extract_with_context(context)

            # Store filters in context
            context.filters = filters

            # Add "filters" step with data immediately (in_progress)
            state_manager.add_run_step(
                run_id=run_id,
                step_id="filters-1",
                step_type="filters",
                message="Understanding your research interests...",
                filters={
                    "topics": filters.topics,
                    "geographical_areas": filters.geographical_areas,
                    "institutions": filters.institutions
                },
                status="in_progress"
            )

            time.sleep(1)  # Brief pause for UX

            # Mark as done (data already visible)
            state_manager.add_run_step(
                run_id=run_id,
                step_id="filters-1",
                step_type="filters",
                message="Understanding your research interests...",
                filters={
                    "topics": filters.topics,
                    "geographical_areas": filters.geographical_areas,
                    "institutions": filters.institutions
                },
                status="done"
            )

        except Exception as e:
            # Mark as done with error
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

            # Add "search" step with papers immediately (in_progress)
            state_manager.add_run_step(
                run_id=run_id,
                step_id="search-1",
                step_type="search",
                message="Looking for relevant papers...",
                papers=preview_papers_dict,
                status="in_progress"
            )

            time.sleep(1.5)  # Brief pause for UX

            # Mark as done (all papers visible)
            state_manager.add_run_step(
                run_id=run_id,
                step_id="search-1",
                step_type="search",
                message="Looking for relevant papers...",
                papers=preview_papers_dict,
                status="done"
            )

        except Exception as e:
            # Mark as done with error
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

        # Add "extraction" step immediately to show in UI (in_progress, no professors yet)
        state_manager.add_run_step(
            run_id=run_id,
            step_id="extraction-1",
            step_type="extraction",
            message="Extracting relevant professors...",
            professors=[],
            status="in_progress"
        )

        try:
            # Extract professors using the agent (this takes time)
            professor_nodes, basic_professors = self.extraction_agent.extract_professors(context)

            # Store full professor nodes in context for final graph construction
            context.professor_nodes = [node.model_dump() for node in professor_nodes]

            # Convert BasicProfessor objects to dict for JSON serialization
            basic_professors_dict = [prof.model_dump() for prof in basic_professors]

            # Update step with professors (still in_progress)
            state_manager.add_run_step(
                run_id=run_id,
                step_id="extraction-1",
                step_type="extraction",
                message="Extracting relevant professors...",
                professors=basic_professors_dict,
                status="in_progress"
            )

            time.sleep(1.5)  # Brief pause for UX

            # Mark as done (all professors visible)
            state_manager.add_run_step(
                run_id=run_id,
                step_id="extraction-1",
                step_type="extraction",
                message="Extracting relevant professors...",
                professors=basic_professors_dict,
                status="done"
            )

        except Exception as e:
            # Mark as done with error
            state_manager.add_run_step(
                run_id=run_id,
                step_id="extraction-1",
                step_type="extraction",
                message=f"Failed to extract professors: {str(e)}",
                status="done"
            )
            raise

    def _execute_relationships(self, context: AgentContext) -> None:
        """
        Step 4: Build relationships between professors.
        """
        run_id = context.run_id

        # Add "relationships" step (in_progress) with message
        state_manager.add_run_step(
            run_id=run_id,
            step_id="relationships-1",
            step_type="relationships",
            message="Analyzing relationships...",
            status="in_progress"
        )

        time.sleep(1)  # Brief pause for UX

        try:
            # Build links from professor nodes
            if not context.professor_nodes:
                raise ValueError("No professor nodes found for relationship building")

            links = build_graph_links(context.professor_nodes)

            # Store links in context (we'll combine with nodes in graph construction)
            context.links = [link.model_dump() for link in links]

            # Update the same step to "done" (same message)
            state_manager.add_run_step(
                run_id=run_id,
                step_id="relationships-1",
                step_type="relationships",
                message="Analyzing relationships...",
                status="done"
            )

        except Exception as e:
            # Mark as done with error
            state_manager.add_run_step(
                run_id=run_id,
                step_id="relationships-1",
                step_type="relationships",
                message=f"Failed to build relationships: {str(e)}",
                status="done"
            )
            raise

    def _execute_graph_construction(self, context: AgentContext) -> None:
        """
        Step 5: Construct final graph with nodes and links.
        """
        run_id = context.run_id

        # Add "graph" step (in_progress) with message
        state_manager.add_run_step(
            run_id=run_id,
            step_id="graph-1",
            step_type="graph",
            message="Building the final graph...",
            status="in_progress"
        )

        time.sleep(1)  # Brief pause for UX

        try:
            # Create User node
            user_node = create_user_node()

            # Combine all nodes (professors + user)
            all_nodes = context.professor_nodes + [user_node.model_dump()]

            # Get links from context
            links = context.links if hasattr(context, 'links') else []

            # Create GraphData
            graph_data = GraphData(
                nodes=[GraphNode(**node) for node in all_nodes],
                links=links
            )

            # Store in state manager
            state_manager.set_run_graph(run_id, graph_data.model_dump())

            # Update the same step to "done" (same message)
            state_manager.add_run_step(
                run_id=run_id,
                step_id="graph-1",
                step_type="graph",
                message="Building the final graph...",
                status="done"
            )

        except Exception as e:
            # Mark as done with error
            state_manager.add_run_step(
                run_id=run_id,
                step_id="graph-1",
                step_type="graph",
                message=f"Failed to construct graph: {str(e)}",
                status="done"
            )
            raise

    def _save_run_to_database(self, context: AgentContext) -> None:
        """
        Save the completed run to the database.
        Saves run_id, query, and graph_data.
        """
        run_id = context.run_id

        try:
            # Get the run data from state manager
            run_data = state_manager.get_run(run_id)

            if not run_data:
                print(f"Warning: No run data found for {run_id}")
                return

            # Get graph data from the run
            graph_data = run_data.get("graph_data")

            # Use the actual query from context
            query = context.query

            # Save to database
            db.create_run(run_id=run_id, query=query, graph_data=graph_data)

            print(f"Successfully saved run {run_id} to database with query: {query}")

        except Exception as e:
            # Log error but don't fail the entire run
            print(f"Error saving run {run_id} to database: {str(e)}")

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
