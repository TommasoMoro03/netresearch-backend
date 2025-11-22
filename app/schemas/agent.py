from pydantic import BaseModel
from typing import List, Optional, Literal


class AgentRunRequest(BaseModel):
    query: str
    cv_id: Optional[str] = None
    max_nodes: int = 10


class AgentRunResponse(BaseModel):
    run_id: str
    status: str


class StepLog(BaseModel):
    step: str
    message: str
    sources: List[str] = []
    timestamp: str


class PersonHierarchy(BaseModel):
    """Person within an entity (lab, organization, etc.)"""
    full_name: str
    role: str
    contact: Optional[str] = None  # email or linkedin URL


class GraphNode(BaseModel):
    """Node in the research graph"""
    id: str
    name: str
    type: str  # "professor", "laboratory", "paper", "institution", etc.
    description: str  # short description of the node
    sources: List[str] = []  # URLs where info was found
    contacts: List[str] = []  # email or website URLs
    hierarchy: Optional[List[PersonHierarchy]] = None  # for entities like labs


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
