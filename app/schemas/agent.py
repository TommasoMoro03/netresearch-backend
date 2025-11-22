from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any


class AgentRunRequest(BaseModel):
    query: str
    cv_id: Optional[str] = None
    max_nodes: int = 10


class AgentRunResponse(BaseModel):
    run_id: str
    status: str

class Source(BaseModel):
    title: str
    url: str
    type: Literal["paper", "author", "institution", "concept"]


class Paper(BaseModel):
    title: str
    link: Optional[str] = None
    abstract: Optional[str] = None
    publication_year: Optional[int] = None
    topic: Optional[str] = None

class BasicProfessor(BaseModel):
    name: str
    institution: Optional[str]
    description: Optional[str] = None

class StepLog(BaseModel):
    step_id: str
    step_type: Literal["intent", "filters", "search", "extraction", "relationships", "graph"]
    message: str
    status: Literal["in_progress", "done", "pending"]
    timestamp: str

    # Step-specific fields (only populated for relevant step types)
    details: Optional[Dict[str, Any]] = None  # Deprecated, use specific fields below
    filters: Optional[Dict[str, List[str]]] = None  # For "filters" step: {"topics": [...], "geographical_areas": [...]}
    papers: Optional[List[Paper]] = None  # For "search" step: list of papers found
    professors: Optional[List[BasicProfessor]] = None  # For "extraction" step: professors associated to the papers, to be shown during reasoning


class PersonHierarchy(BaseModel):
    """Person within an entity (lab, organization, etc.)"""
    full_name: str
    role: str
    contact: Optional[str] = None  # email or linkedin URL


class Contact(BaseModel):
    email: Optional[str] = None
    website: Optional[str] = None


class GraphNode(BaseModel):
    """Node in the research graph"""
    id: str
    name: str
    type: str  # "professor", "laboratory"
    institution: Optional[str] = None # affiliated institution to the professor
    description: str  # short description of the professor/lab
    contacts: Contact
    works_count: Optional[int] = None  # number of publications
    cited_by_count: Optional[int] = None  # number of citations
    h_index: Optional[int] = None  # h-index for professors
    link_orcid: Optional[str] = None  # ORCID link for professors
    papers: Optional[List[Paper]] = None  # list of papers


class GraphLink(BaseModel):
    """Link between two nodes"""
    source: str  # node id
    target: str  # node id
    label: Optional[str] = None  # relationship type (e.g., "works_at", "collaborates_with")


class GraphData(BaseModel):
    nodes: List[GraphNode]
    links: List[GraphLink]


class AgentStatusResponse(BaseModel):
    run_id: str
    status: Literal["running", "completed"]
    steps: List[StepLog]
    graph_data: Optional[GraphData] = None
