from fastapi import APIRouter, File, UploadFile
from app.schemas.cv import CVUploadResponse
from app.services.state_manager import state_manager
import uuid

router = APIRouter(prefix="/api/cv", tags=["CV"])


@router.post("/upload", response_model=CVUploadResponse)
async def upload_cv(file: UploadFile = File(...)):
    """
    Upload a CV (PDF file) and extract concepts.
    """
    # Generate unique CV ID
    cv_id = str(uuid.uuid4())

    # Read file content (for future processing)
    content = await file.read()

    # Mock extracted concepts for now
    extracted_concepts = ["AI", "Robotics", "Machine Learning"]

    # Store in state manager
    state_manager.store_cv(cv_id, {
        "cv_id": cv_id,
        "filename": file.filename,
        "concepts": extracted_concepts
    })

    return CVUploadResponse(
        cv_id=cv_id,
        message="CV processed",
        extracted_concepts=extracted_concepts
    )
