"""
Data models for agent operations.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ExtractedFilters(BaseModel):
    """Filters extracted from user query and CV"""
    topics: List[str]
    geographical_areas: List[str]  # ISO 3166-1 alpha-2 country codes (e.g., "CH", "US", "FR")
    institutions: List[str]  # University/institution names mentioned in query


class AgentContext(BaseModel):
    """Context for agent execution"""
    run_id: str
    query: str
    cv_id: Optional[str] = None
    cv_concepts: Optional[List[str]] = None
    max_nodes: int = 10

    # Extracted information during execution
    filters: Optional[ExtractedFilters] = None
    papers_data: Optional[List[Dict[str, Any]]] = None  # Full OpenAlex papers JSON for later processing
    professor_nodes: Optional[List[Any]] = None  # GraphNode objects for final graph (stored as dicts)
    links: Optional[List[Any]] = None  # GraphLink objects for final graph (stored as dicts)
