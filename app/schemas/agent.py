from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime


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


class GraphNode(BaseModel):
    id: str
    label: str
    type: str  # "paper", "author", "concept", etc.
    x: float
    y: float
    z: float


class GraphLink(BaseModel):
    source: str
    target: str
    label: Optional[str] = None


class GraphData(BaseModel):
    nodes: List[GraphNode]
    links: List[GraphLink]


class AgentStatusResponse(BaseModel):
    run_id: str
    status: Literal["running", "completed"]
    steps: List[StepLog]
    graph_data: Optional[GraphData] = None
