from typing import Dict, Any, Optional
from datetime import datetime


class StateManager:
    """In-memory state manager for hackathon purposes."""

    def __init__(self):
        self.cv_store: Dict[str, Dict[str, Any]] = {}
        self.run_store: Dict[str, Dict[str, Any]] = {}

    # CV Management
    def store_cv(self, cv_id: str, cv_data: Dict[str, Any]) -> None:
        """Store CV data."""
        self.cv_store[cv_id] = cv_data

    def get_cv(self, cv_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve CV data."""
        return self.cv_store.get(cv_id)

    def list_cvs(self) -> Dict[str, Dict[str, Any]]:
        """List all CVs."""
        return self.cv_store

    # Run Management
    def create_run(self, run_id: str, query: str, cv_id: Optional[str] = None, max_nodes: int = 10) -> None:
        """Initialize a new agent run."""
        self.run_store[run_id] = {
            "run_id": run_id,
            "query": query,
            "cv_id": cv_id,
            "max_nodes": max_nodes,
            "status": "running",
            "steps": [],
            "graph_data": None,
            "created_at": datetime.utcnow().isoformat()
        }

    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve run state."""
        return self.run_store.get(run_id)

    def update_run_status(self, run_id: str, status: str) -> None:
        """Update run status."""
        if run_id in self.run_store:
            self.run_store[run_id]["status"] = status

    def add_run_step(
        self,
        run_id: str,
        step_id: str,
        step_type: str,
        message: str,
        status: str = "done",
        details: Optional[Dict[str, Any]] = None,
        filters: Optional[Dict[str, Any]] = None,
        papers: Optional[list] = None,
        sources: Optional[list] = None
    ) -> None:
        """
        Add a step log to a run.

        Args:
            run_id: Run identifier
            step_id: Unique step identifier
            step_type: Type of step (intent, filters, search, extraction, relationships, graph)
            message: Human-readable message
            status: Step status (in_progress, done, pending)
            details: Optional details dict (deprecated)
            filters: For "filters" step: {"topics": [...], "geographical_areas": [...]}
            papers: For "search" step: list of Paper objects
            sources: For "extraction" step: list of Source objects
        """
        if run_id in self.run_store:
            step_log = {
                "step_id": step_id,
                "step_type": step_type,
                "message": message,
                "status": status,
                "timestamp": datetime.utcnow().isoformat()
            }

            # Add step-specific fields only if provided
            if details is not None:
                step_log["details"] = details
            if filters is not None:
                step_log["filters"] = filters
            if papers is not None:
                step_log["papers"] = papers
            if sources is not None:
                step_log["sources"] = sources

            self.run_store[run_id]["steps"].append(step_log)

    def set_run_graph(self, run_id: str, graph_data: Dict[str, Any]) -> None:
        """Set the graph data for a completed run."""
        if run_id in self.run_store:
            self.run_store[run_id]["graph_data"] = graph_data

    def list_runs(self) -> Dict[str, Dict[str, Any]]:
        """List all runs."""
        return self.run_store


# Global state manager instance
state_manager = StateManager()
