from fastapi import APIRouter
from pydantic import BaseModel
from app.services.state_manager import state_manager
from app.database.database import db

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

    # Save to database
    user = db.get_user()
    if user:
        # User exists, update name
        db.update_user_name(request.name)
    else:
        # No user exists yet, create one with empty CV
        db.create_user(request.name, "")

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


@router.get("/user")
async def get_user_data():
    """
    Get user data from database (name and CV status).
    """
    user = db.get_user()

    if user:
        return {
            "name": user["name"],
            "has_cv": bool(user["cv_transcribed"] and user["cv_transcribed"].strip())
        }

    return {
        "name": "",
        "has_cv": False
    }


@router.post("/clean")
async def clean_history():
    """
    Reset all data in the database (delete all users and runs).
    """
    try:
        db.reset_all_data()
        # Also clear in-memory state
        state_manager.cv_store.clear()
        state_manager.run_store.clear()
        state_manager.user_name = None

        return {
            "message": "History cleaned successfully",
            "status": "success"
        }
    except Exception as e:
        return {
            "message": f"Failed to clean history: {str(e)}",
            "status": "error"
        }


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
