from fastapi import APIRouter
from pydantic import BaseModel
from app.services.state_manager import state_manager

router = APIRouter(prefix="/api", tags=["User"])


class UserNameRequest(BaseModel):
    name: str


class UserNameResponse(BaseModel):
    message: str
    name: str


@router.post("/name", response_model=UserNameResponse)
async def set_user_name(request: UserNameRequest):
    """
    Store the user's name for use in emails and visualization.
    """
    state_manager.set_user_name(request.name)
    
    return UserNameResponse(
        message="User name stored successfully",
        name=request.name
    )


@router.get("/name", response_model=UserNameResponse)
async def get_user_name():
    """
    Retrieve the stored user name.
    """
    name = state_manager.get_user_name()
    
    return UserNameResponse(
        message="User name retrieved successfully",
        name=name or "Anonymous"
    )


@router.get("/debug")
async def debug_state():
    """
    Debug endpoint to check current state.
    """
    return {
        "user_name": state_manager.get_user_name(),
        "cv_count": len(state_manager.cv_store),
        "run_count": len(state_manager.run_store)
    }
