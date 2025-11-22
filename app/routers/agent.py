from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.schemas.agent import AgentRunRequest, AgentRunResponse, AgentStatusResponse
from app.services.state_manager import state_manager
from app.services.simulation_service import simulate_agent_run
import uuid

router = APIRouter(prefix="/api/agent", tags=["Agent"])


@router.post("/run", response_model=AgentRunResponse)
async def start_agent_run(request: AgentRunRequest, background_tasks: BackgroundTasks):
    """
    Start a new agent run.
    Initializes the run state and starts background processing.
    """
    # Generate unique run ID
    run_id = str(uuid.uuid4())

    # Create run in state manager
    state_manager.create_run(
        run_id=run_id,
        query=request.query,
        cv_id=request.cv_id,
        max_nodes=request.max_nodes
    )

    # Start background simulation
    background_tasks.add_task(
        simulate_agent_run,
        run_id=run_id,
        query=request.query,
        max_nodes=request.max_nodes
    )

    return AgentRunResponse(run_id=run_id, status="started")


@router.get("/status/{run_id}", response_model=AgentStatusResponse)
async def get_agent_status(run_id: str):
    """
    Poll the status of an agent run.
    Returns current status, steps, and graph data (when completed).
    """
    run_data = state_manager.get_run(run_id)

    if not run_data:
        raise HTTPException(status_code=404, detail="Run not found")

    return AgentStatusResponse(
        run_id=run_data["run_id"],
        status=run_data["status"],
        steps=run_data["steps"],
        graph_data=run_data["graph_data"]
    )
